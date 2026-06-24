from __future__ import annotations

import pytest

from tecsoo_letolto.core.error_mapping import (
    map_exception,
    map_subprocess_failure,
    user_error_text,
)
from tecsoo_letolto.core.errors import (
    NetworkError,
    NotEnoughSpaceError,
    OutputDirectoryError,
    RestrictedContentError,
    UnsupportedUrlError,
    YtDlpError,
)


@pytest.mark.parametrize(
    ("stderr", "expected"),
    [
        ("ERROR: Unsupported URL: https://example.invalid", UnsupportedUrlError),
        ("ERROR: Private video. Sign in if you have been granted access.", RestrictedContentError),
        ("ERROR: The read operation timed out", NetworkError),
        ("ERROR: Permission denied: target.mp3", OutputDirectoryError),
        ("ERROR: No space left on device", NotEnoughSpaceError),
    ],
)
def test_map_subprocess_failure_known_categories(stderr: str, expected: type[Exception]) -> None:
    assert isinstance(map_subprocess_failure("yt-dlp", 1, "", stderr), expected)


def test_map_subprocess_failure_defaults_to_ytdlp_error() -> None:
    error = map_subprocess_failure("yt-dlp", 1, "", "ERROR: unexpected")
    assert isinstance(error, YtDlpError)
    assert error.technical_detail == "ERROR: unexpected"


def test_map_exception_wraps_permission_error() -> None:
    assert isinstance(map_exception(PermissionError("denied")), OutputDirectoryError)


def test_user_error_text_is_hungarian_and_actionable() -> None:
    text = user_error_text(RestrictedContentError())
    assert "Valószínű ok:" in text
    assert "Mit próbálhatsz meg:" in text
    assert "cookie" in text
