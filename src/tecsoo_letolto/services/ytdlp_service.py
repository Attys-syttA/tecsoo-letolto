from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from tecsoo_letolto.core.errors import ToolMissingError, YtDlpError
from tecsoo_letolto.core.paths import app_base_dir
from tecsoo_letolto.utils.subprocess_runner import ProcessResult, run_checked


DownloadMode = Literal["audio", "video"]
AudioFormat = Literal["mp3", "m4a", "opus", "wav"]
VideoFormat = Literal["mp4", "mkv"]
Quality = Literal["normal", "good", "best"]


@dataclass(frozen=True)
class YtDlpTool:
    executable: Path
    version: str


@dataclass(frozen=True)
class RuntimeTools:
    ytdlp: YtDlpTool
    ffmpeg_dir: Path


@dataclass(frozen=True)
class DownloadRequest:
    url: str
    output_dir: Path
    filename_base: str | None
    mode: DownloadMode
    audio_format: AudioFormat = "mp3"
    video_format: VideoFormat = "mp4"
    quality: Quality = "good"


def find_packaged_ytdlp(base_dir: Path | None = None, runner=run_checked) -> YtDlpTool:
    root = base_dir or app_base_dir()
    executable = root / "vendor" / "yt-dlp" / "yt-dlp.exe"
    if not executable.is_file():
        raise ToolMissingError(
            "Hiányzik a yt-dlp.exe a portable csomagból.",
            technical_detail=f"Missing yt-dlp: {executable}",
        )
    result: ProcessResult = runner([str(executable), "--version"], timeout=8)
    if result.returncode != 0:
        raise YtDlpError(technical_detail=result.stderr or result.stdout)
    return YtDlpTool(executable=executable, version=(result.stdout or "").strip())


def quality_format_selector(mode: DownloadMode, quality: Quality) -> str:
    if mode == "audio":
        return "bestaudio/best"
    if quality == "normal":
        return "bv*[height<=720]+ba/best[height<=720]/best"
    if quality == "good":
        return "bv*[height<=1080]+ba/best[height<=1080]/best"
    return "bv*+ba/best"


def audio_quality_value(quality: Quality) -> str:
    return {
        "normal": "128",
        "good": "192",
        "best": "0",
    }[quality]


def build_output_template(request: DownloadRequest, output_path: Path) -> str:
    if request.filename_base:
        return str(output_path)
    return str(request.output_dir / "%(title).180B_%(upload_date>%Y-%m-%d)s.%(ext)s")


def build_ytdlp_args(request: DownloadRequest, tools: RuntimeTools, output_path: Path) -> list[str]:
    args = [
        str(tools.ytdlp.executable),
        "--ffmpeg-location",
        str(tools.ffmpeg_dir),
        "--no-playlist",
        "--newline",
        "--no-overwrites",
        "-f",
        quality_format_selector(request.mode, request.quality),
        "-o",
        build_output_template(request, output_path),
    ]

    if request.mode == "audio":
        args.extend(
            [
                "--extract-audio",
                "--audio-format",
                request.audio_format,
                "--audio-quality",
                audio_quality_value(request.quality),
            ]
        )
    else:
        args.extend(["--merge-output-format", request.video_format])

    args.append(request.url)
    return args
