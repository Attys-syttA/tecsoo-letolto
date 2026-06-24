from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from tecsoo_letolto.core.filename_policy import sanitize_filename_base
from tecsoo_letolto.core.paths import default_output_dir
from tecsoo_letolto.services.ytdlp_service import DownloadRequest

ALLOWED_AUDIO_FORMATS = {"mp3", "m4a", "opus", "wav"}
ALLOWED_VIDEO_FORMATS = {"mp4", "mkv"}
ALLOWED_MODES = {"audio", "video"}
ALLOWED_QUALITIES = {"normal", "good", "best"}


@dataclass
class DownloadFormState:
    url: str = ""
    output_dir: str = ""
    filename: str = ""
    mode: str = "audio"
    audio_format: str = "mp3"
    video_format: str = "mp4"
    quality: str = "good"


def _is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_form(state: DownloadFormState) -> list[str]:
    errors: list[str] = []
    url = state.url.strip()
    if not url:
        errors.append("Add meg a letöltendő linket.")
    elif not _is_http_url(url):
        errors.append("A linknek http:// vagy https:// kezdetű webcímnek kell lennie.")

    if state.mode not in ALLOWED_MODES:
        errors.append("Ismeretlen letöltési mód.")
    if state.audio_format not in ALLOWED_AUDIO_FORMATS:
        errors.append("Ismeretlen hangformátum.")
    if state.video_format not in ALLOWED_VIDEO_FORMATS:
        errors.append("Ismeretlen videóformátum.")
    if state.quality not in ALLOWED_QUALITIES:
        errors.append("Ismeretlen minőségi beállítás.")
    return errors


def output_dir_from_state(state: DownloadFormState) -> Path:
    raw = state.output_dir.strip()
    if not raw:
        return default_output_dir()
    return Path(raw).expanduser()


def to_download_request(state: DownloadFormState) -> DownloadRequest:
    errors = validate_form(state)
    if errors:
        raise ValueError("\n".join(errors))

    filename_base = sanitize_filename_base(state.filename) if state.filename.strip() else None
    return DownloadRequest(
        url=state.url.strip(),
        output_dir=output_dir_from_state(state),
        filename_base=filename_base,
        mode=state.mode,  # type: ignore[arg-type]
        audio_format=state.audio_format,  # type: ignore[arg-type]
        video_format=state.video_format,  # type: ignore[arg-type]
        quality=state.quality,  # type: ignore[arg-type]
    )
