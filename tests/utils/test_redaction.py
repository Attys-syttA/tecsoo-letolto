from __future__ import annotations

from tecsoo_letolto.utils.redaction import redact_path, redact_text


def test_redact_text_masks_key_value_secrets() -> None:
    assert redact_text("password=abc token=def api_key=ghi") == (
        "password=<redacted> token=<redacted> api_key=<redacted>"
    )


def test_redact_text_masks_bearer_token() -> None:
    assert redact_text("Authorization: Bearer abc.def.ghi") == "Authorization: Bearer <redacted>"


def test_redact_path_masks_windows_user_name() -> None:
    assert redact_path(r"C:\Users\Bíró Attila\Downloads\file.mp3") == r"C:\...\Downloads\file.mp3"
