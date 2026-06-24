from __future__ import annotations

import subprocess
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProcessResult:
    args: list[str]
    returncode: int
    stdout: str
    stderr: str


class RunningProcess:
    def __init__(self, process: subprocess.Popen[str]) -> None:
        self._process = process

    @property
    def returncode(self) -> int | None:
        return self._process.poll()

    def cancel(self) -> None:
        if self._process.poll() is not None:
            return
        self._process.terminate()

    def wait(self, timeout: float | None = None) -> int:
        return self._process.wait(timeout=timeout)


def _creation_flags() -> int:
    return getattr(subprocess, "CREATE_NO_WINDOW", 0)


def run_checked(args: list[str], timeout: int = 30, cwd: Path | None = None) -> ProcessResult:
    completed = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
        creationflags=_creation_flags(),
    )
    return ProcessResult(
        args=list(args),
        returncode=completed.returncode,
        stdout=completed.stdout or "",
        stderr=completed.stderr or "",
    )


def start_streaming(
    args: list[str],
    cwd: Path | None = None,
    on_stdout_line: Callable[[str], None] | None = None,
    on_stderr_line: Callable[[str], None] | None = None,
) -> RunningProcess:
    process = subprocess.Popen(
        args,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=_creation_flags(),
    )
    # Streaming readers are intentionally left to the caller's worker thread in
    # the first implementation slice. This wrapper owns safe process startup and
    # cancellation without forcing a threading model yet.
    _ = on_stdout_line, on_stderr_line
    return RunningProcess(process)


def run_streaming(
    args: list[str],
    *,
    timeout: int = 30,
    cwd: Path | None = None,
    on_line: Callable[[str], None] | None = None,
    should_cancel: Callable[[], bool] | None = None,
) -> ProcessResult:
    process = subprocess.Popen(
        args,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        creationflags=_creation_flags(),
    )
    stdout_lines: list[str] = []
    started = time.monotonic()
    assert process.stdout is not None
    while True:
        if should_cancel and should_cancel() and process.poll() is None:
            process.terminate()
        if timeout and time.monotonic() - started > timeout and process.poll() is None:
            process.kill()
            return ProcessResult(args=list(args), returncode=-1, stdout="".join(stdout_lines), stderr="timeout")
        line = process.stdout.readline()
        if line:
            stdout_lines.append(line)
            if on_line:
                on_line(line.rstrip("\r\n"))
            continue
        if process.poll() is not None:
            break
        time.sleep(0.05)
    return ProcessResult(args=list(args), returncode=process.returncode or 0, stdout="".join(stdout_lines), stderr="")


def join_args_for_log(args: Iterable[str]) -> str:
    return " ".join(f'"{arg}"' if " " in arg else arg for arg in args)
