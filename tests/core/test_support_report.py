from __future__ import annotations

from datetime import datetime

from tecsoo_letolto.core.support_report import (
    SupportContext,
    build_support_report,
    mailto_url,
    sanitize_url_for_report,
    tail_log_lines,
)


def test_sanitize_url_for_report_keeps_domain_and_video_id_only() -> None:
    url = "https://www.youtube.com/watch?v=abc123&token=secret&list=private"
    assert sanitize_url_for_report(url) == "www.youtube.com/watch?v=abc123"


def test_sanitize_url_for_report_shortens_path() -> None:
    assert sanitize_url_for_report("https://example.test/a/b/c") == "example.test/.../c"


def test_tail_log_lines_limits_and_redacts(tmp_path) -> None:
    log = tmp_path / "app.log"
    log.write_text("\n".join(f"line {i} token=secret{i}" for i in range(100)), encoding="utf-8")

    lines = tail_log_lines(log, max_lines=3)

    assert len(lines) == 3
    assert lines[0].startswith("line 97")
    assert "secret" not in "\n".join(lines)
    assert "token=<redacted>" in lines[0]


def test_build_support_report_redacts_sensitive_values() -> None:
    context = SupportContext(
        app_version="0.1.0-dev",
        windows_version="Windows",
        ytdlp_version="2026.06.01",
        ffmpeg_version="ffmpeg version 7",
        last_error_category="ytdlp",
        last_error_summary="failed with password=abc",
        output_dir_writable=True,
        mode="audio",
        timestamp=datetime(2026, 6, 24, 18, 30),
        url="https://example.test/watch?v=id&cookie=abc",
    )

    report = build_support_report(context, [r"C:\Users\Bíró Attila\Downloads token=abc"])

    assert "password=<redacted>" in report
    assert "cookie=abc" not in report
    assert r"C:\...\Downloads" in report
    assert "example.test/watch?v=id" in report


def test_mailto_url_contains_support_address_and_encoded_subject() -> None:
    url = mailto_url("teszt")
    assert url.startswith("mailto:attys@e-sper.hu?")
    assert "TecsoLetolto+hibajelent" in url
