from __future__ import annotations

import sys
from pathlib import Path

import pytest

from tecsoo_letolto.core.errors import OutputDirectoryError
from tecsoo_letolto.core import paths


def test_user_downloads_dir_prefers_userprofile(monkeypatch) -> None:
    monkeypatch.setenv("USERPROFILE", r"C:\Users\Teszt Elek")
    assert paths.user_downloads_dir() == Path(r"C:\Users\Teszt Elek") / "Downloads"


def test_user_downloads_dir_falls_back_to_home(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("USERPROFILE", raising=False)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    assert paths.user_downloads_dir() == tmp_path / "Downloads"


def test_default_output_dir_is_downloads(monkeypatch) -> None:
    monkeypatch.setenv("USERPROFILE", r"C:\Users\Bíró Attila")
    assert paths.default_output_dir() == Path(r"C:\Users\Bíró Attila") / "Downloads"


def test_local_app_data_dir_prefers_localappdata(monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", r"C:\Users\Test\AppData\Local")
    assert paths.local_app_data_dir() == Path(r"C:\Users\Test\AppData\Local") / "TecsoLetolto"


def test_logs_dir_is_under_local_app_data(monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", r"C:\Users\Test\AppData\Local")
    assert paths.logs_dir() == Path(r"C:\Users\Test\AppData\Local") / "TecsoLetolto" / "logs"


def test_app_base_dir_uses_executable_when_frozen(monkeypatch, tmp_path) -> None:
    fake_exe = tmp_path / "TecsoLetolto.exe"
    fake_exe.write_text("", encoding="utf-8")
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(fake_exe))

    assert paths.app_base_dir() == tmp_path


def test_release_vendor_dir_is_under_app_base_dir(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(paths, "app_base_dir", lambda: tmp_path)
    assert paths.release_vendor_dir() == tmp_path / "vendor"


def test_ensure_writable_dir_creates_directory(tmp_path) -> None:
    target = tmp_path / "új letöltések"
    paths.ensure_writable_dir(target)
    assert target.is_dir()


def test_ensure_writable_dir_wraps_write_failures(monkeypatch, tmp_path) -> None:
    target = tmp_path / "target"

    def raise_permission_error(self, *args, **kwargs):
        raise PermissionError("denied")

    monkeypatch.setattr(Path, "write_text", raise_permission_error)

    with pytest.raises(OutputDirectoryError):
        paths.ensure_writable_dir(target)
