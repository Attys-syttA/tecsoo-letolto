from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from .errors import FilenameConflictError

WINDOWS_ILLEGAL_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1F\x7F]')
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}
MAX_FILENAME_BASE_LENGTH = 180


def sanitize_filename_base(value: str, fallback: str = "letoltes") -> str:
    base = WINDOWS_ILLEGAL_CHARS.sub("_", value or "").strip()
    base = base.rstrip(". ")
    if not base:
        base = fallback
    if base.upper() in WINDOWS_RESERVED_NAMES:
        base = f"{base}_"
    if len(base) > MAX_FILENAME_BASE_LENGTH:
        base = base[:MAX_FILENAME_BASE_LENGTH].rstrip(". ")
    return base or fallback


def _normalize_extension(extension: str) -> str:
    normalized = extension.strip().lstrip(".")
    if not normalized:
        raise ValueError("extension must not be empty")
    return sanitize_filename_base(normalized, fallback="bin")


def build_default_filename(
    title: str | None,
    extension: str,
    now: datetime | None = None,
) -> str:
    timestamp = now or datetime.now()
    safe_extension = _normalize_extension(extension)
    if title and title.strip():
        base = sanitize_filename_base(f"{title}_{timestamp:%Y-%m-%d}")
    else:
        base = sanitize_filename_base(f"letoltes_{timestamp:%Y-%m-%d}_{timestamp:%H%M%S}")
    return f"{base}.{safe_extension}"


def split_name_and_extension(filename: str) -> tuple[str, str]:
    path = Path(filename)
    extension = path.suffix.lstrip(".")
    base = path.stem if extension else path.name
    return base, extension


def next_available_path(directory: Path, filename: str) -> Path:
    base, extension = split_name_and_extension(filename)
    safe_base = sanitize_filename_base(base)
    safe_extension = _normalize_extension(extension) if extension else ""
    candidate_name = f"{safe_base}.{safe_extension}" if safe_extension else safe_base
    candidate = directory / candidate_name
    if not candidate.exists():
        return candidate

    for index in range(1, 100):
        numbered = f"{safe_base}_{index:02d}"
        candidate_name = f"{numbered}.{safe_extension}" if safe_extension else numbered
        candidate = directory / candidate_name
        if not candidate.exists():
            return candidate

    raise FilenameConflictError(
        technical_detail=f"No free filename after 99 attempts in {directory}"
    )
