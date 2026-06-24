from __future__ import annotations

import sys

from tecsoo_letolto.utils.subprocess_runner import join_args_for_log, run_checked


def test_run_checked_captures_successful_process() -> None:
    result = run_checked([sys.executable, "-c", "print('ok')"])

    assert result.returncode == 0
    assert result.stdout.strip() == "ok"
    assert result.stderr == ""


def test_run_checked_captures_stderr_and_return_code() -> None:
    result = run_checked(
        [sys.executable, "-c", "import sys; print('bad', file=sys.stderr); raise SystemExit(7)"]
    )

    assert result.returncode == 7
    assert result.stderr.strip() == "bad"


def test_join_args_for_log_quotes_arguments_with_spaces() -> None:
    assert join_args_for_log(["yt-dlp.exe", "--output", "C:/Users/Test Folder/file.mp3"]) == (
        'yt-dlp.exe --output "C:/Users/Test Folder/file.mp3"'
    )
