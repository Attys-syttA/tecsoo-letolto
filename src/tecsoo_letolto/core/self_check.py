from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tecsoo_letolto.core.paths import default_output_dir, ensure_writable_dir, logs_dir
from tecsoo_letolto.services.ffmpeg_service import find_packaged_ffmpeg
from tecsoo_letolto.services.ytdlp_service import find_packaged_ytdlp
from tecsoo_letolto.version import __version__


@dataclass(frozen=True)
class SelfCheckItem:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class SelfCheckResult:
    ok: bool
    items: list[SelfCheckItem]


def run_self_check(base_dir: Path | None = None) -> SelfCheckResult:
    items: list[SelfCheckItem] = [
        SelfCheckItem("app-version", True, __version__),
    ]

    try:
        ensure_writable_dir(logs_dir())
        items.append(SelfCheckItem("logs-dir-writable", True, str(logs_dir())))
    except Exception as exc:
        items.append(SelfCheckItem("logs-dir-writable", False, str(exc)))

    try:
        ensure_writable_dir(default_output_dir())
        items.append(SelfCheckItem("downloads-dir-writable", True, str(default_output_dir())))
    except Exception as exc:
        items.append(SelfCheckItem("downloads-dir-writable", False, str(exc)))

    try:
        ytdlp = find_packaged_ytdlp(base_dir)
        items.append(SelfCheckItem("yt-dlp", True, ytdlp.version))
    except Exception as exc:
        items.append(SelfCheckItem("yt-dlp", False, str(exc)))

    try:
        ffmpeg = find_packaged_ffmpeg(base_dir)
        items.append(SelfCheckItem("ffmpeg", True, ffmpeg.version))
    except Exception as exc:
        items.append(SelfCheckItem("ffmpeg", False, str(exc)))

    return SelfCheckResult(ok=all(item.ok for item in items), items=items)
