from __future__ import annotations

from dataclasses import dataclass

from tecsoo_letolto.core import self_check


@dataclass(frozen=True)
class FakeYtDlp:
    version: str = "2026.06.01"


@dataclass(frozen=True)
class FakeFfmpeg:
    version: str = "ffmpeg version 7"


def test_run_self_check_reports_all_green_when_dependencies_exist(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(self_check, "logs_dir", lambda: tmp_path / "logs")
    monkeypatch.setattr(self_check, "default_output_dir", lambda: tmp_path / "downloads")
    monkeypatch.setattr(self_check, "find_packaged_ytdlp", lambda base_dir=None: FakeYtDlp())
    monkeypatch.setattr(self_check, "find_packaged_ffmpeg", lambda base_dir=None: FakeFfmpeg())

    result = self_check.run_self_check(tmp_path)

    assert result.ok is True
    assert {item.name for item in result.items} == {
        "app-version",
        "logs-dir-writable",
        "downloads-dir-writable",
        "yt-dlp",
        "ffmpeg",
    }


def test_run_self_check_marks_missing_vendor_as_failure(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(self_check, "logs_dir", lambda: tmp_path / "logs")
    monkeypatch.setattr(self_check, "default_output_dir", lambda: tmp_path / "downloads")
    monkeypatch.setattr(self_check, "find_packaged_ytdlp", lambda base_dir=None: (_ for _ in ()).throw(RuntimeError("missing")))
    monkeypatch.setattr(self_check, "find_packaged_ffmpeg", lambda base_dir=None: FakeFfmpeg())

    result = self_check.run_self_check(tmp_path)

    assert result.ok is False
    assert any(item.name == "yt-dlp" and not item.ok for item in result.items)
