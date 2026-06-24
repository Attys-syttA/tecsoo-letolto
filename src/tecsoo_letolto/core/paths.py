from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

from .errors import OutputDirectoryError

APP_NAME = "TecsoLetolto"


def user_downloads_dir() -> Path:
    user_profile = os.environ.get("USERPROFILE")
    if user_profile:
        return Path(user_profile) / "Downloads"
    return Path.home() / "Downloads"


def default_output_dir() -> Path:
    return user_downloads_dir()


def local_app_data_dir() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / APP_NAME
    return Path.home() / f".{APP_NAME}"


def logs_dir() -> Path:
    return local_app_data_dir() / "logs"


def app_base_dir() -> Path:
    if bool(getattr(sys, "frozen", False)):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[3]


def packaged_resource_dir() -> Path:
    pyinstaller_root = getattr(sys, "_MEIPASS", None)
    if pyinstaller_root:
        return Path(pyinstaller_root)
    return Path(__file__).resolve().parents[1] / "resources"


def release_vendor_dir() -> Path:
    return app_base_dir() / "vendor"


def ensure_writable_dir(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / f".tecsoletolto_write_test_{uuid.uuid4().hex}.tmp"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except Exception as exc:
        raise OutputDirectoryError(
            "A mentési mappa nem hozható létre vagy nem írható.",
            technical_detail=str(exc),
            cause=exc,
        ) from exc
