from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MediaInfo:
    title: str | None
    webpage_url: str
    extractor: str | None = None
    duration_seconds: int | None = None
    id: str | None = None
