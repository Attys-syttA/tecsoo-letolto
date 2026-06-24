from __future__ import annotations

from pathlib import Path

import pytest

from tecsoo_letolto.core.download_manager import DownloadManager, choose_output_path, expected_extension
from tecsoo_letolto.core.errors import DownloadCancelledError, RestrictedContentError
from tecsoo_letolto.core.progress import CancelToken, ProgressEvent
from tecsoo_letolto.services.ytdlp_service import DownloadRequest
from tecsoo_letolto.utils.subprocess_runner import ProcessResult


def _make_vendor(root: Path) -> None:
    ffmpeg_dir = root / "vendor" / "ffmpeg" / "bin"
    ytdlp_dir = root / "vendor" / "yt-dlp"
    ffmpeg_dir.mkdir(parents=True)
    ytdlp_dir.mkdir(parents=True)
    (ffmpeg_dir / "ffmpeg.exe").write_text("", encoding="utf-8")
    (ffmpeg_dir / "ffprobe.exe").write_text("", encoding="utf-8")
    (ytdlp_dir / "yt-dlp.exe").write_text("", encoding="utf-8")


def test_expected_extension_uses_mode_format(tmp_path) -> None:
    assert expected_extension(
        DownloadRequest(url="https://example.test", output_dir=tmp_path, filename_base="a", mode="audio", audio_format="m4a")
    ) == "m4a"
    assert expected_extension(
        DownloadRequest(url="https://example.test", output_dir=tmp_path, filename_base="v", mode="video", video_format="mkv")
    ) == "mkv"


def test_choose_output_path_uses_filename_base_and_conflict_suffix(tmp_path) -> None:
    (tmp_path / "zene.mp3").write_text("existing", encoding="utf-8")
    request = DownloadRequest(
        url="https://example.test",
        output_dir=tmp_path,
        filename_base="zene",
        mode="audio",
        audio_format="mp3",
    )

    assert choose_output_path(request) == tmp_path / "zene_01.mp3"


def test_download_manager_runs_ytdlp_with_vendor_tools(tmp_path) -> None:
    _make_vendor(tmp_path)
    calls: list[list[str]] = []

    def runner(args, timeout=30, cwd=None):
        calls.append(args)
        if args[-1] == "--version":
            return ProcessResult(args=args, returncode=0, stdout="2026.06.01\n", stderr="")
        if args[1] == "-version":
            return ProcessResult(args=args, returncode=0, stdout="ffmpeg version 7\n", stderr="")
        return ProcessResult(args=args, returncode=0, stdout="download ok", stderr="")

    def streaming_runner(args, timeout=30, cwd=None, on_line=None, should_cancel=None):
        calls.append(args)
        if on_line:
            on_line("[download]  50.0% of 1.00MiB")
        return ProcessResult(args=args, returncode=0, stdout="download ok", stderr="")

    request = DownloadRequest(
        url="https://example.test/video",
        output_dir=tmp_path / "downloads",
        filename_base="teszt",
        mode="audio",
    )

    events: list[ProgressEvent] = []

    class Sink:
        def publish(self, event: ProgressEvent) -> None:
            events.append(event)

    result = DownloadManager(base_dir=tmp_path, runner=runner, streaming_runner=streaming_runner).run(
        request,
        progress_sink=Sink(),
    )

    assert result.output_path == tmp_path / "downloads" / "teszt.mp3"
    assert any("yt-dlp.exe" in call[0] and "--no-playlist" in call for call in calls)
    assert any(event.percent == 50 for event in events)
    assert events[-1].phase == "done"


def test_download_manager_maps_ytdlp_errors(tmp_path) -> None:
    _make_vendor(tmp_path)

    def runner(args, timeout=30, cwd=None):
        if args[-1] == "--version":
            return ProcessResult(args=args, returncode=0, stdout="2026.06.01\n", stderr="")
        if args[1] == "-version":
            return ProcessResult(args=args, returncode=0, stdout="ffmpeg version 7\n", stderr="")
        return ProcessResult(args=args, returncode=1, stdout="", stderr="ERROR: Private video. Sign in.")

    def streaming_runner(args, timeout=30, cwd=None, on_line=None, should_cancel=None):
        return ProcessResult(args=args, returncode=1, stdout="", stderr="ERROR: Private video. Sign in.")

    request = DownloadRequest(
        url="https://example.test/video",
        output_dir=tmp_path / "downloads",
        filename_base="teszt",
        mode="audio",
    )

    with pytest.raises(RestrictedContentError):
        DownloadManager(base_dir=tmp_path, runner=runner, streaming_runner=streaming_runner).run(request)


def test_download_manager_cancel_token_stops_download(tmp_path) -> None:
    _make_vendor(tmp_path)

    def runner(args, timeout=30, cwd=None):
        if args[-1] == "--version":
            return ProcessResult(args=args, returncode=0, stdout="2026.06.01\n", stderr="")
        if args[1] == "-version":
            return ProcessResult(args=args, returncode=0, stdout="ffmpeg version 7\n", stderr="")
        return ProcessResult(args=args, returncode=0, stdout="", stderr="")

    token = CancelToken()

    def streaming_runner(args, timeout=30, cwd=None, on_line=None, should_cancel=None):
        token.cancel()
        assert should_cancel is not None
        assert should_cancel()
        return ProcessResult(args=args, returncode=1, stdout="", stderr="")

    request = DownloadRequest(
        url="https://example.test/video",
        output_dir=tmp_path / "downloads",
        filename_base="teszt",
        mode="audio",
    )

    with pytest.raises(DownloadCancelledError):
        DownloadManager(base_dir=tmp_path, runner=runner, streaming_runner=streaming_runner).run(
            request,
            cancel_token=token,
        )
