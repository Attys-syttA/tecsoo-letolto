from __future__ import annotations

from pathlib import Path

import pytest

from tecsoo_letolto.gui import view_model
from tecsoo_letolto.gui.view_model import DownloadFormState, to_download_request, validate_form


def test_validate_form_requires_url() -> None:
    assert validate_form(DownloadFormState()) == ["Add meg a letöltendő linket."]


def test_validate_form_rejects_non_http_url() -> None:
    errors = validate_form(DownloadFormState(url="ftp://example.test/file"))
    assert "http:// vagy https://" in errors[0]


def test_validate_form_rejects_unknown_options() -> None:
    errors = validate_form(
        DownloadFormState(
            url="https://example.test/video",
            mode="playlist",
            audio_format="flac",
            video_format="avi",
            quality="raw",
        )
    )

    assert errors == [
        "Ismeretlen letöltési mód.",
        "Ismeretlen hangformátum.",
        "Ismeretlen videóformátum.",
        "Ismeretlen minőségi beállítás.",
    ]


def test_to_download_request_uses_downloads_default(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(view_model, "default_output_dir", lambda: tmp_path / "Downloads")

    request = to_download_request(DownloadFormState(url="https://example.test/video"))

    assert request.output_dir == tmp_path / "Downloads"
    assert request.mode == "audio"
    assert request.audio_format == "mp3"
    assert request.quality == "good"


def test_to_download_request_sanitizes_optional_filename() -> None:
    request = to_download_request(
        DownloadFormState(
            url="https://example.test/video",
            output_dir=r"C:\Users\Test\Downloads",
            filename="CON",
            mode="video",
            video_format="mkv",
            quality="best",
        )
    )

    assert request.output_dir == Path(r"C:\Users\Test\Downloads")
    assert request.filename_base == "CON_"
    assert request.mode == "video"
    assert request.video_format == "mkv"


def test_to_download_request_raises_on_invalid_form() -> None:
    with pytest.raises(ValueError):
        to_download_request(DownloadFormState(url="not a url"))
