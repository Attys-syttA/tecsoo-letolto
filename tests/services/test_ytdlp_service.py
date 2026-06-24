from __future__ import annotations

from pathlib import Path

import pytest

from tecsoo_letolto.core.errors import ToolMissingError
from tecsoo_letolto.services.ytdlp_service import (
    DownloadRequest,
    RuntimeTools,
    YtDlpTool,
    audio_quality_value,
    build_ytdlp_args,
    find_packaged_ytdlp,
    quality_format_selector,
)
from tecsoo_letolto.utils.subprocess_runner import ProcessResult


def _runner(args, timeout=30, cwd=None):
    return ProcessResult(args=args, returncode=0, stdout="2026.06.01\n", stderr="")


def _tools(tmp_path) -> RuntimeTools:
    return RuntimeTools(
        ytdlp=YtDlpTool(executable=tmp_path / "vendor" / "yt-dlp" / "yt-dlp.exe", version="2026.06.01"),
        ffmpeg_dir=tmp_path / "vendor" / "ffmpeg" / "bin",
    )


def test_find_packaged_ytdlp_reads_version(tmp_path) -> None:
    ytdlp_dir = tmp_path / "vendor" / "yt-dlp"
    ytdlp_dir.mkdir(parents=True)
    (ytdlp_dir / "yt-dlp.exe").write_text("", encoding="utf-8")

    tool = find_packaged_ytdlp(tmp_path, runner=_runner)

    assert tool.executable == ytdlp_dir / "yt-dlp.exe"
    assert tool.version == "2026.06.01"


def test_find_packaged_ytdlp_reports_missing_tool(tmp_path) -> None:
    with pytest.raises(ToolMissingError):
        find_packaged_ytdlp(tmp_path, runner=_runner)


def test_quality_format_selector_video_modes() -> None:
    assert quality_format_selector("video", "normal") == "bv*[height<=720]+ba/best[height<=720]/best"
    assert quality_format_selector("video", "good") == "bv*[height<=1080]+ba/best[height<=1080]/best"
    assert quality_format_selector("video", "best") == "bv*+ba/best"


def test_audio_quality_value() -> None:
    assert audio_quality_value("normal") == "128"
    assert audio_quality_value("good") == "192"
    assert audio_quality_value("best") == "0"


def test_build_ytdlp_args_for_audio(tmp_path) -> None:
    request = DownloadRequest(
        url="https://example.test/watch?v=abc",
        output_dir=tmp_path,
        filename_base="teszt",
        mode="audio",
        audio_format="mp3",
        quality="good",
    )
    output_path = tmp_path / "teszt.mp3"

    args = build_ytdlp_args(request, _tools(tmp_path), output_path)

    assert "--no-playlist" in args
    assert "--newline" in args
    assert "--extract-audio" in args
    assert args[args.index("--audio-format") + 1] == "mp3"
    assert args[args.index("--audio-quality") + 1] == "192"
    assert args[args.index("-o") + 1] == str(output_path)
    assert args[-1] == request.url


def test_build_ytdlp_args_for_video(tmp_path) -> None:
    request = DownloadRequest(
        url="https://example.test/watch?v=abc",
        output_dir=tmp_path,
        filename_base="video",
        mode="video",
        video_format="mkv",
        quality="best",
    )
    output_path = tmp_path / "video.mkv"

    args = build_ytdlp_args(request, _tools(tmp_path), output_path)

    assert "--extract-audio" not in args
    assert args[args.index("--merge-output-format") + 1] == "mkv"
    assert args[args.index("-f") + 1] == "bv*+ba/best"
