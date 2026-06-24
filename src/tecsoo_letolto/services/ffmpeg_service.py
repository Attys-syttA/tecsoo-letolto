from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from tecsoo_letolto.core.errors import FfmpegError, ToolMissingError
from tecsoo_letolto.core.paths import app_base_dir
from tecsoo_letolto.utils.subprocess_runner import ProcessResult, run_checked


@dataclass(frozen=True)
class FfmpegTools:
    ffmpeg: Path
    ffprobe: Path
    version: str


def _candidate_dirs(base_dir: Path) -> list[Path]:
    candidates = [
        base_dir / "vendor" / "ffmpeg" / "bin",
        base_dir / "ffmpeg" / "bin",
    ]
    dev_override = os.environ.get("TECSOLETOLTO_DEV_FFMPEG_DIR")
    if dev_override:
        candidates.append(Path(dev_override))
    return candidates


def find_packaged_ffmpeg(
    base_dir: Path | None = None,
    runner=run_checked,
) -> FfmpegTools:
    root = base_dir or app_base_dir()
    for candidate in _candidate_dirs(root):
        ffmpeg = candidate / "ffmpeg.exe"
        ffprobe = candidate / "ffprobe.exe"
        if ffmpeg.is_file() and ffprobe.is_file():
            return check_ffmpeg(ffmpeg, ffprobe, runner=runner)
    raise ToolMissingError(
        "Hiányzik az FFmpeg a portable csomagból.",
        technical_detail=f"Checked under {root}",
    )


def check_ffmpeg(ffmpeg: Path, ffprobe: Path, runner=run_checked) -> FfmpegTools:
    if not ffmpeg.is_file():
        raise ToolMissingError(technical_detail=f"Missing ffmpeg: {ffmpeg}")
    if not ffprobe.is_file():
        raise ToolMissingError(technical_detail=f"Missing ffprobe: {ffprobe}")

    result: ProcessResult = runner([str(ffmpeg), "-version"], timeout=8)
    if result.returncode != 0:
        raise FfmpegError(technical_detail=result.stderr or result.stdout)

    first_line = (result.stdout or "").splitlines()[0].strip() if result.stdout else "ffmpeg version unknown"
    return FfmpegTools(ffmpeg=ffmpeg, ffprobe=ffprobe, version=first_line)
