from __future__ import annotations

from pathlib import Path

import pytest

from tecsoo_letolto.core.errors import ToolMissingError
from tecsoo_letolto.services.ffmpeg_service import check_ffmpeg, find_packaged_ffmpeg
from tecsoo_letolto.utils.subprocess_runner import ProcessResult


def _runner(args, timeout=30, cwd=None):
    return ProcessResult(args=args, returncode=0, stdout="ffmpeg version 7.0-test\nmore", stderr="")


def test_find_packaged_ffmpeg_uses_vendor_bin(tmp_path) -> None:
    vendor_bin = tmp_path / "vendor" / "ffmpeg" / "bin"
    vendor_bin.mkdir(parents=True)
    (vendor_bin / "ffmpeg.exe").write_text("", encoding="utf-8")
    (vendor_bin / "ffprobe.exe").write_text("", encoding="utf-8")

    tools = find_packaged_ffmpeg(tmp_path, runner=_runner)

    assert tools.ffmpeg == vendor_bin / "ffmpeg.exe"
    assert tools.ffprobe == vendor_bin / "ffprobe.exe"
    assert tools.version == "ffmpeg version 7.0-test"


def test_check_ffmpeg_requires_ffprobe(tmp_path) -> None:
    ffmpeg = tmp_path / "ffmpeg.exe"
    ffmpeg.write_text("", encoding="utf-8")

    with pytest.raises(ToolMissingError):
        check_ffmpeg(ffmpeg, tmp_path / "ffprobe.exe", runner=_runner)


def test_find_packaged_ffmpeg_reports_missing_tool(tmp_path) -> None:
    with pytest.raises(ToolMissingError):
        find_packaged_ffmpeg(tmp_path, runner=_runner)
