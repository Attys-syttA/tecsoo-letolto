from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tecsoo_letolto.core.error_mapping import map_subprocess_failure
from tecsoo_letolto.core.errors import DownloadCancelledError
from tecsoo_letolto.core.filename_policy import build_default_filename, next_available_path
from tecsoo_letolto.core.paths import ensure_writable_dir
from tecsoo_letolto.core.progress import CancelToken, ProgressEvent, ProgressSink, parse_ytdlp_progress_line
from tecsoo_letolto.services.ffmpeg_service import find_packaged_ffmpeg
from tecsoo_letolto.services.ytdlp_service import (
    DownloadRequest,
    RuntimeTools,
    build_ytdlp_args,
    find_packaged_ytdlp,
)
from tecsoo_letolto.utils.subprocess_runner import ProcessResult, run_checked, run_streaming


@dataclass(frozen=True)
class DownloadResult:
    output_path: Path
    stdout: str
    stderr: str


def expected_extension(request: DownloadRequest) -> str:
    if request.mode == "audio":
        return request.audio_format
    return request.video_format


def choose_output_path(request: DownloadRequest) -> Path:
    extension = expected_extension(request)
    if request.filename_base:
        filename = f"{request.filename_base}.{extension}"
    else:
        filename = build_default_filename(None, extension)
    return next_available_path(request.output_dir, filename)


class DownloadManager:
    def __init__(
        self,
        *,
        base_dir: Path | None = None,
        runner=run_checked,
        streaming_runner=run_streaming,
    ) -> None:
        self._base_dir = base_dir
        self._runner = runner
        self._streaming_runner = streaming_runner

    def run(
        self,
        request: DownloadRequest,
        *,
        progress_sink: ProgressSink | None = None,
        cancel_token: CancelToken | None = None,
    ) -> DownloadResult:
        ensure_writable_dir(request.output_dir)
        ffmpeg = find_packaged_ffmpeg(self._base_dir, runner=self._runner)
        ytdlp = find_packaged_ytdlp(self._base_dir, runner=self._runner)
        output_path = choose_output_path(request)
        tools = RuntimeTools(ytdlp=ytdlp, ffmpeg_dir=ffmpeg.ffmpeg.parent)
        args = build_ytdlp_args(request, tools, output_path)
        if progress_sink:
            progress_sink.publish(ProgressEvent("preparing", None, "Letöltés indítása..."))

        def on_line(line: str) -> None:
            if not progress_sink:
                return
            event = parse_ytdlp_progress_line(line)
            if event:
                progress_sink.publish(event)

        result: ProcessResult = self._streaming_runner(
            args,
            timeout=60 * 60,
            on_line=on_line,
            should_cancel=cancel_token.is_cancelled if cancel_token else None,
        )
        if cancel_token and cancel_token.is_cancelled():
            if progress_sink:
                progress_sink.publish(ProgressEvent("error", None, "Letöltés megszakítva."))
            raise DownloadCancelledError()
        if result.returncode != 0:
            raise map_subprocess_failure("yt-dlp", result.returncode, result.stdout, result.stderr)
        if progress_sink:
            progress_sink.publish(ProgressEvent("done", 100, "Letöltés kész."))

        return DownloadResult(output_path=output_path, stdout=result.stdout, stderr=result.stderr)
