from __future__ import annotations

import json
import shutil
import hashlib
from dataclasses import dataclass
import urllib.request
from pathlib import Path

from tecsoo_letolto.core.errors import ToolUpdateError
from tecsoo_letolto.services.ytdlp_service import YtDlpTool
from tecsoo_letolto.utils.subprocess_runner import ProcessResult, run_checked

YT_DLP_LATEST_API_URL = "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"
YT_DLP_EXE_DOWNLOAD_URL = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
YT_DLP_SHA256SUMS_URL = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/SHA2-256SUMS"


@dataclass(frozen=True)
class YtDlpUpdateResult:
    current_version: str
    previous_version: str
    sha256: str
    backup_path: Path


def get_current_ytdlp_version(tool: YtDlpTool, runner=run_checked) -> str:
    result: ProcessResult = runner([str(tool.executable), "--version"], timeout=8)
    if result.returncode != 0:
        raise ToolUpdateError(technical_detail=result.stderr or result.stdout)
    return (result.stdout or "").strip()


def get_latest_ytdlp_version(urlopen=urllib.request.urlopen) -> str:
    with urlopen(YT_DLP_LATEST_API_URL, timeout=15) as response:
        payload = json.loads(response.read().decode("utf-8"))
    tag = str(payload.get("tag_name") or "").strip()
    if not tag:
        raise ToolUpdateError(technical_detail="GitHub latest release response did not contain tag_name")
    return tag.removeprefix("yt-dlp-")


def download_ytdlp_release(temp_dir: Path, urlretrieve=urllib.request.urlretrieve) -> Path:
    temp_dir.mkdir(parents=True, exist_ok=True)
    target = temp_dir / "yt-dlp.exe"
    urlretrieve(YT_DLP_EXE_DOWNLOAD_URL, target)
    if not target.is_file():
        raise ToolUpdateError(technical_detail=f"Downloaded file missing: {target}")
    return target


def calculate_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def parse_sha256_sums(text: str, filename: str = "yt-dlp.exe") -> str:
    expected_name = filename.lower()
    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        candidate = parts[-1].lstrip("*").replace("\\", "/").split("/")[-1].lower()
        if candidate == expected_name:
            return parts[0].lower()
    raise ToolUpdateError(technical_detail=f"SHA2-256SUMS did not contain {filename}")


def verify_ytdlp_sha256(
    exe: Path,
    checksum_text: str | None = None,
    urlopen=urllib.request.urlopen,
) -> str:
    if checksum_text is None:
        with urlopen(YT_DLP_SHA256SUMS_URL, timeout=15) as response:
            checksum_text = response.read().decode("utf-8")
    expected_hash = parse_sha256_sums(checksum_text)
    actual_hash = calculate_sha256(exe)
    if actual_hash.lower() != expected_hash.lower():
        raise ToolUpdateError(
            technical_detail=f"yt-dlp.exe SHA256 mismatch: expected {expected_hash}, got {actual_hash}"
        )
    return actual_hash


def verify_downloaded_ytdlp(exe: Path, runner=run_checked) -> str:
    if exe.name.lower() != "yt-dlp.exe":
        raise ToolUpdateError(technical_detail=f"Unexpected yt-dlp filename: {exe.name}")
    result: ProcessResult = runner([str(exe), "--version"], timeout=8)
    if result.returncode != 0:
        raise ToolUpdateError(technical_detail=result.stderr or result.stdout)
    version = (result.stdout or "").strip()
    if not version:
        raise ToolUpdateError(technical_detail="yt-dlp --version returned empty output")
    return version


def replace_with_backup(current: Path, new_file: Path) -> Path:
    if current.name.lower() != "yt-dlp.exe":
        raise ToolUpdateError(technical_detail=f"Refusing to replace non yt-dlp.exe file: {current}")
    if new_file.name.lower() != "yt-dlp.exe":
        raise ToolUpdateError(technical_detail=f"Refusing to install unexpected file: {new_file}")
    if not current.is_file():
        raise ToolUpdateError(technical_detail=f"Current yt-dlp missing: {current}")
    if not new_file.is_file():
        raise ToolUpdateError(technical_detail=f"New yt-dlp missing: {new_file}")

    previous = current.with_name("yt-dlp.previous.exe")
    if previous.exists():
        previous.unlink()
    current.replace(previous)
    try:
        shutil.copy2(new_file, current)
    except Exception:
        rollback(previous, current)
        raise
    return previous


def rollback(previous: Path, current: Path) -> None:
    if not previous.is_file():
        raise ToolUpdateError(technical_detail=f"Previous yt-dlp missing: {previous}")
    if current.exists():
        current.unlink()
    previous.replace(current)


def install_latest_ytdlp(
    current: Path,
    temp_dir: Path,
    *,
    previous_version: str,
    runner=run_checked,
) -> YtDlpUpdateResult:
    new_file = download_ytdlp_release(temp_dir)
    sha256 = verify_ytdlp_sha256(new_file)
    new_version = verify_downloaded_ytdlp(new_file, runner=runner)
    previous = replace_with_backup(current, new_file)
    try:
        installed_version = verify_downloaded_ytdlp(current, runner=runner)
    except Exception:
        rollback(previous, current)
        raise
    if installed_version != new_version:
        rollback(previous, current)
        raise ToolUpdateError(
            technical_detail=f"Installed yt-dlp version mismatch: expected {new_version}, got {installed_version}"
        )
    return YtDlpUpdateResult(
        current_version=installed_version,
        previous_version=previous_version,
        sha256=sha256,
        backup_path=previous,
    )
