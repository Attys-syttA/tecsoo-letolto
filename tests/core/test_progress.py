from __future__ import annotations

from tecsoo_letolto.core.progress import parse_ytdlp_progress_line


def test_parse_download_percent_line() -> None:
    event = parse_ytdlp_progress_line("[download]  12.3% of 10.00MiB at 1.00MiB/s ETA 00:09")

    assert event is not None
    assert event.phase == "downloading"
    assert event.percent == 12.3


def test_parse_postprocessing_line() -> None:
    event = parse_ytdlp_progress_line("[ExtractAudio] Destination: out.mp3")

    assert event is not None
    assert event.phase == "postprocessing"
    assert event.percent is None


def test_parse_ignores_unrelated_line() -> None:
    assert parse_ytdlp_progress_line("plain output") is None
