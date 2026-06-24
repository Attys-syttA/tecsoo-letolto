from __future__ import annotations

from datetime import datetime

import pytest

from tecsoo_letolto.core.errors import FilenameConflictError
from tecsoo_letolto.core.filename_policy import (
    MAX_FILENAME_BASE_LENGTH,
    build_default_filename,
    next_available_path,
    sanitize_filename_base,
    split_name_and_extension,
)


def test_sanitize_filename_base_replaces_windows_illegal_characters() -> None:
    assert sanitize_filename_base('a<b>c:d"e/f\\g|h?i*j') == "a_b_c_d_e_f_g_h_i_j"


def test_sanitize_filename_base_uses_fallback_for_empty_or_dot_only_name() -> None:
    assert sanitize_filename_base("   ...  ") == "letoltes"
    assert sanitize_filename_base("", fallback="audio") == "audio"


def test_sanitize_filename_base_avoids_reserved_windows_names() -> None:
    assert sanitize_filename_base("CON") == "CON_"
    assert sanitize_filename_base("lpt1") == "lpt1_"


def test_sanitize_filename_base_truncates_long_values() -> None:
    value = "a" * (MAX_FILENAME_BASE_LENGTH + 20)
    assert sanitize_filename_base(value) == "a" * MAX_FILENAME_BASE_LENGTH


def test_build_default_filename_uses_title_and_date() -> None:
    now = datetime(2026, 6, 24, 17, 45, 12)
    assert build_default_filename("Teszt: cím", "mp3", now) == "Teszt_ cím_2026-06-24.mp3"


def test_build_default_filename_uses_timestamp_without_title() -> None:
    now = datetime(2026, 6, 24, 17, 45, 12)
    assert build_default_filename(None, ".m4a", now) == "letoltes_2026-06-24_174512.m4a"


def test_split_name_and_extension() -> None:
    assert split_name_and_extension("sample.name.mp3") == ("sample.name", "mp3")
    assert split_name_and_extension("sample") == ("sample", "")


def test_next_available_path_returns_original_when_free(tmp_path) -> None:
    assert next_available_path(tmp_path, "zene.mp3") == tmp_path / "zene.mp3"


def test_next_available_path_adds_number_suffix(tmp_path) -> None:
    (tmp_path / "zene.mp3").write_text("existing", encoding="utf-8")
    (tmp_path / "zene_01.mp3").write_text("existing", encoding="utf-8")

    assert next_available_path(tmp_path, "zene.mp3") == tmp_path / "zene_02.mp3"


def test_next_available_path_raises_after_99_conflicts(tmp_path) -> None:
    (tmp_path / "zene.mp3").write_text("existing", encoding="utf-8")
    for index in range(1, 100):
        (tmp_path / f"zene_{index:02d}.mp3").write_text("existing", encoding="utf-8")

    with pytest.raises(FilenameConflictError):
        next_available_path(tmp_path, "zene.mp3")
