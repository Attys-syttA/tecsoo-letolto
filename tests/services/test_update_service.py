from __future__ import annotations

import io
import hashlib

import pytest

from tecsoo_letolto.core.errors import ToolUpdateError
from tecsoo_letolto.services.update_service import (
    calculate_sha256,
    download_ytdlp_release,
    get_current_ytdlp_version,
    get_latest_ytdlp_version,
    install_latest_ytdlp,
    parse_sha256_sums,
    replace_with_backup,
    rollback,
    verify_downloaded_ytdlp,
    verify_ytdlp_sha256,
)
from tecsoo_letolto.services.ytdlp_service import YtDlpTool
from tecsoo_letolto.utils.subprocess_runner import ProcessResult


class FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return None

    def read(self):
        return b'{"tag_name": "2026.06.01"}'


def test_get_current_ytdlp_version() -> None:
    def runner(args, timeout=30, cwd=None):
        return ProcessResult(args=args, returncode=0, stdout="2026.06.01\n", stderr="")

    version = get_current_ytdlp_version(YtDlpTool(executable="yt-dlp.exe", version="old"), runner=runner)

    assert version == "2026.06.01"


def test_get_latest_ytdlp_version_from_github_payload() -> None:
    version = get_latest_ytdlp_version(urlopen=lambda url, timeout=15: FakeResponse())
    assert version == "2026.06.01"


def test_download_ytdlp_release_writes_expected_file(tmp_path) -> None:
    def urlretrieve(url, target):
        target.write_bytes(b"exe")
        return target, None

    downloaded = download_ytdlp_release(tmp_path, urlretrieve=urlretrieve)

    assert downloaded == tmp_path / "yt-dlp.exe"
    assert downloaded.read_bytes() == b"exe"


def test_parse_sha256_sums_finds_windows_binary() -> None:
    text = "0" * 64 + "  yt-dlp\n" + "a" * 64 + " *yt-dlp.exe\n"

    assert parse_sha256_sums(text) == "a" * 64


def test_verify_ytdlp_sha256_checks_downloaded_file(tmp_path) -> None:
    exe = tmp_path / "yt-dlp.exe"
    exe.write_bytes(b"exe")
    digest = hashlib.sha256(b"exe").hexdigest()

    assert verify_ytdlp_sha256(exe, checksum_text=f"{digest}  yt-dlp.exe\n") == digest


def test_calculate_sha256_reads_file(tmp_path) -> None:
    exe = tmp_path / "yt-dlp.exe"
    exe.write_bytes(b"abc")

    assert calculate_sha256(exe) == hashlib.sha256(b"abc").hexdigest()


def test_verify_downloaded_ytdlp_rejects_unexpected_name(tmp_path) -> None:
    exe = tmp_path / "other.exe"
    exe.write_text("", encoding="utf-8")

    with pytest.raises(ToolUpdateError):
        verify_downloaded_ytdlp(exe)


def test_replace_with_backup_and_rollback(tmp_path) -> None:
    current = tmp_path / "yt-dlp.exe"
    new_file = tmp_path / "incoming" / "yt-dlp.exe"
    new_file.parent.mkdir()
    current.write_text("old", encoding="utf-8")
    new_file.write_text("new", encoding="utf-8")

    previous = replace_with_backup(current, new_file)

    assert previous.name == "yt-dlp.previous.exe"
    assert previous.read_text(encoding="utf-8") == "old"
    assert current.read_text(encoding="utf-8") == "new"

    rollback(previous, current)

    assert current.read_text(encoding="utf-8") == "old"


def test_replace_with_backup_refuses_non_ytdlp_target(tmp_path) -> None:
    current = tmp_path / "TecsoLetolto.exe"
    new_file = tmp_path / "yt-dlp.exe"
    current.write_text("app", encoding="utf-8")
    new_file.write_text("new", encoding="utf-8")

    with pytest.raises(ToolUpdateError):
        replace_with_backup(current, new_file)


def test_install_latest_ytdlp_replaces_only_current_binary(monkeypatch, tmp_path) -> None:
    current = tmp_path / "vendor" / "yt-dlp" / "yt-dlp.exe"
    temp_dir = tmp_path / "temp"
    current.parent.mkdir(parents=True)
    current.write_bytes(b"old")

    def fake_download(target_dir):
        target_dir.mkdir(parents=True)
        downloaded = target_dir / "yt-dlp.exe"
        downloaded.write_bytes(b"new")
        return downloaded

    def fake_sha256(path):
        return "a" * 64

    def fake_verify(path, runner):
        return "2026.06.09" if path.read_bytes() == b"new" else "old"

    monkeypatch.setattr("tecsoo_letolto.services.update_service.download_ytdlp_release", fake_download)
    monkeypatch.setattr("tecsoo_letolto.services.update_service.verify_ytdlp_sha256", fake_sha256)
    monkeypatch.setattr("tecsoo_letolto.services.update_service.verify_downloaded_ytdlp", fake_verify)

    result = install_latest_ytdlp(current, temp_dir, previous_version="old")

    assert current.read_bytes() == b"new"
    assert result.current_version == "2026.06.09"
    assert result.previous_version == "old"
    assert result.backup_path.name == "yt-dlp.previous.exe"
