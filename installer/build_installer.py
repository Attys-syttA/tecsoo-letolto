from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


DEFAULT_FFMPEG_DIR = r"E:\ffmpeg-2026-04-09-git-d3d0b7a5ee-essentials_build\bin"


def _copy_ffmpeg_bin(ffmpeg_dir: Path, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Copy the whole bin dir (exes, optional dlls) so the portable package
    # doesn't depend on machine-local codecs/binaries.
    # Still validate the minimum expected tools exist.
    needed = ["ffmpeg.exe", "ffprobe.exe"]
    missing = [n for n in needed if not (ffmpeg_dir / n).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing in {ffmpeg_dir}: {', '.join(missing)}")

    for src in ffmpeg_dir.iterdir():
        if not src.is_file():
            continue
        shutil.copy2(src, dest_dir / src.name)


def _make_payload_zip(payload_dir: Path, out_zip: Path) -> None:
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(out_zip, "w", compression=ZIP_DEFLATED, compresslevel=9) as zf:
        for path in payload_dir.rglob("*"):
            if path.is_dir():
                continue
            arcname = path.relative_to(payload_dir).as_posix()
            zf.write(path, arcname)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build payload.zip for the self-extracting installer.")
    parser.add_argument(
        "--ffmpeg-dir",
        default=None,
        help=f"FFmpeg bin dir (default: {DEFAULT_FFMPEG_DIR})",
    )
    parser.add_argument(
        "--gui-exe",
        default=str(Path("dist") / "TecsoLetolto.exe"),
        help="Path to built GUI exe (PyInstaller output).",
    )
    parser.add_argument(
        "--out-zip",
        default=str(Path("installer") / "payload.zip"),
        help="Output zip path.",
    )
    parser.add_argument(
        "--out-dirname",
        default="TecsoLetolto",
        help="Folder name created on extract.",
    )
    args = parser.parse_args(argv)

    gui_exe = Path(args.gui_exe).resolve()
    if not gui_exe.is_file():
        raise FileNotFoundError(f"GUI exe not found: {gui_exe}")

    ffmpeg_dir = Path(args.ffmpeg_dir or DEFAULT_FFMPEG_DIR).resolve()
    if not ffmpeg_dir.is_dir():
        raise FileNotFoundError(f"FFmpeg dir not found: {ffmpeg_dir}")

    payload_root = Path("installer") / "_payload" / args.out_dirname
    if payload_root.exists():
        shutil.rmtree(payload_root)
    payload_root.mkdir(parents=True, exist_ok=True)

    shutil.copy2(gui_exe, payload_root / gui_exe.name)
    _copy_ffmpeg_bin(ffmpeg_dir, payload_root / "ffmpeg" / "bin")

    readme = payload_root / "README_PORTABLE.txt"
    readme.write_text(
        "TecsoLetolto portable package\n"
        "\n"
        "Run: TecsoLetolto.exe\n"
        "\n"
        "Bundled ffmpeg is in: .\\ffmpeg\\bin\n"
        "If you want to override, set environment variable FFMPEG_DIR.\n",
        encoding="utf-8",
    )

    out_zip = Path(args.out_zip).resolve()
    if out_zip.is_file():
        out_zip.unlink()
    _make_payload_zip(payload_root.parent, out_zip)
    print(f"Wrote {out_zip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
