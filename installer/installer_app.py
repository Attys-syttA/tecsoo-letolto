from __future__ import annotations

import io
import shutil
import sys
import traceback
import zipfile
from pathlib import Path
from tkinter import Tk, messagebox
from tkinter import filedialog


def _resource_path(name: str) -> Path:
    # PyInstaller onefile: resources are unpacked into sys._MEIPASS
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / name


def _ask_target_dir() -> Path | None:
    root = Tk()
    root.withdraw()
    root.update()
    target = filedialog.askdirectory(title="Válaszd ki a telepítés helyét (mappát)")
    root.destroy()
    if not target:
        return None
    return Path(target).expanduser().resolve()


def _safe_extract_zip(zip_bytes: bytes, target_dir: Path) -> None:
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        for member in zf.infolist():
            name = member.filename
            if name.endswith("/"):
                continue
            dest = (target_dir / name).resolve()
            if target_dir not in dest.parents and dest != target_dir:
                raise RuntimeError(f"Unsafe path in archive: {name}")
        zf.extractall(target_dir)


def _zip_single_top_dir(zip_bytes: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        top: set[str] = set()
        for info in zf.infolist():
            name = info.filename.strip("/")
            if not name:
                continue
            first = name.split("/", 1)[0]
            if first:
                top.add(first)
        if len(top) != 1:
            raise RuntimeError(f"Installer payload must contain a single top-level folder, got: {sorted(top)}")
        return next(iter(top))


def _confirm_existing_install() -> str | None:
    root = Tk()
    root.withdraw()
    root.update()
    res = messagebox.askyesnocancel(
        "Már létezik",
        "A kiválasztott célmappában már létezik egy TecsoLetolto telepítés.\n\n"
        "Igen: fájlok felülírása (a régi extra fájlok megmaradhatnak)\n"
        "Nem: törlés és tiszta újratelepítés\n"
        "Mégse: megszakítás",
        icon="warning",
    )
    root.destroy()
    if res is None:
        return None
    return "overwrite" if res else "clean"


def main() -> int:
    try:
        payload_path = _resource_path("payload.zip")
        payload = payload_path.read_bytes()

        target_dir = _ask_target_dir()
        if target_dir is None:
            return 0

        top_dir = _zip_single_top_dir(payload)
        install_dir = (target_dir / top_dir).resolve()
        if target_dir not in install_dir.parents:
            raise RuntimeError("Invalid install directory computed.")

        if install_dir.exists():
            action = _confirm_existing_install()
            if action is None:
                return 0
            if action == "clean":
                shutil.rmtree(install_dir)

        _safe_extract_zip(payload, target_dir)

        root = Tk()
        root.withdraw()
        messagebox.showinfo(
            "Kész",
            f"Kicsomagolva ide:\n{target_dir}\n\nA program indítása:\n{top_dir}\\TecsoLetolto.exe",
        )
        root.destroy()
        return 0
    except Exception:
        err = traceback.format_exc()
        try:
            root = Tk()
            root.withdraw()
            messagebox.showerror("Hiba", err)
            root.destroy()
        except Exception:
            pass
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
