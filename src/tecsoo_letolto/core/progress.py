from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Literal, Protocol


@dataclass(frozen=True)
class ProgressEvent:
    phase: Literal["preparing", "downloading", "postprocessing", "done", "error"]
    percent: float | None
    message: str


class ProgressSink(Protocol):
    def publish(self, event: ProgressEvent) -> None: ...


class CancelToken:
    def __init__(self) -> None:
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    def is_cancelled(self) -> bool:
        return self._cancelled


def parse_ytdlp_progress_line(line: str) -> ProgressEvent | None:
    value = line.strip()
    if not value:
        return None
    if value.startswith("[download]"):
        match = re.search(r"(\d+(?:\.\d+)?)%", value)
        if match:
            return ProgressEvent("downloading", float(match.group(1)), value)
        if "100%" in value or "Destination:" in value:
            return ProgressEvent("downloading", None, value)
        return ProgressEvent("downloading", None, value)
    if value.startswith("[ExtractAudio]") or value.startswith("[Merger]") or value.startswith("[ffmpeg]"):
        return ProgressEvent("postprocessing", None, value)
    if "Deleting original file" in value:
        return ProgressEvent("postprocessing", None, value)
    return None
