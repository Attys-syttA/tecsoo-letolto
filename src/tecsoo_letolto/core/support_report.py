from __future__ import annotations

import platform
import urllib.parse
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from tecsoo_letolto.utils.redaction import redact_path, redact_text

SUPPORT_EMAIL = "attys@e-sper.hu"
SUPPORT_SUBJECT = "TecsoLetolto hibajelentés"


@dataclass(frozen=True)
class SupportContext:
    app_version: str
    windows_version: str | None
    ytdlp_version: str | None
    ffmpeg_version: str | None
    last_error_category: str | None
    last_error_summary: str | None
    output_dir_writable: bool | None
    mode: str | None
    timestamp: datetime
    url: str | None = None


def current_windows_version() -> str:
    return platform.platform()


def sanitize_url_for_report(url: str | None) -> str | None:
    if not url:
        return None
    parsed = urllib.parse.urlparse(url)
    if not parsed.netloc:
        return "<redacted-url>"
    host = parsed.netloc
    query = urllib.parse.parse_qs(parsed.query)
    video_id = query.get("v", [None])[0]
    if video_id:
        return f"{host}{parsed.path}?v={video_id}"
    if parsed.path and parsed.path != "/":
        safe_path = parsed.path.rstrip("/").split("/")[-1]
        return f"{host}/.../{safe_path}"
    return host


def tail_log_lines(log_path: Path, max_lines: int = 60) -> list[str]:
    if not log_path.is_file():
        return []
    lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    return [redact_text(line) for line in lines[-max_lines:]]


def _value(value: object) -> str:
    if value is None:
        return "n/a"
    return str(value)


def build_support_report(context: SupportContext, log_lines: list[str]) -> str:
    url = sanitize_url_for_report(context.url)
    lines = [
        "TecsoLetolto hibajelentés",
        "",
        f"Program verzió: {context.app_version}",
        f"Windows verzió: {_value(context.windows_version)}",
        f"yt-dlp verzió: {_value(context.ytdlp_version)}",
        f"FFmpeg verzió: {_value(context.ffmpeg_version)}",
        f"Hiba kategória: {_value(context.last_error_category)}",
        f"Hiba rövid leírás: {redact_text(_value(context.last_error_summary))}",
        f"Célmappa írható: {_value(context.output_dir_writable)}",
        f"Letöltési mód: {_value(context.mode)}",
        f"Időpont: {context.timestamp.isoformat(timespec='seconds')}",
        f"Link rövidítve: {_value(url)}",
        "",
        "Utolsó releváns naplósorok:",
    ]
    if log_lines:
        lines.extend(redact_path(redact_text(line)) for line in log_lines)
    else:
        lines.append("n/a")
    return "\n".join(lines)


def mailto_url(report: str) -> str:
    query = urllib.parse.urlencode({"subject": SUPPORT_SUBJECT, "body": report})
    return f"mailto:{SUPPORT_EMAIL}?{query}"


def open_mailto(report: str) -> bool:
    return webbrowser.open(mailto_url(report))
