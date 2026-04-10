from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
import re

import yt_dlp


DEFAULT_FFMPEG_DIR = r"E:\ffmpeg-2026-04-09-git-d3d0b7a5ee-essentials_build\bin"


def _find_ffmpeg_dir(cli_value: str | None) -> str | None:
    if cli_value:
        return cli_value
    env_value = os.environ.get("FFMPEG_DIR") or os.environ.get("YTDLP_FFMPEG_DIR")
    if env_value:
        return env_value
    if Path(DEFAULT_FFMPEG_DIR).is_dir():
        return DEFAULT_FFMPEG_DIR
    return None


def _ffmpeg_exe(ffmpeg_dir: str) -> Path:
    return Path(ffmpeg_dir) / "ffmpeg.exe"


def _check_ffmpeg(ffmpeg_dir: str) -> tuple[bool, str]:
    exe = _ffmpeg_exe(ffmpeg_dir)
    if not exe.is_file():
        return False, f"Nem találom az ffmpeg-et itt: {exe}"
    try:
        p = subprocess.run(
            [str(exe), "-version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=8,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except Exception as e:
        return False, f"Nem tudtam futtatni az ffmpeg-et ({exe}): {e}"
    if p.returncode != 0:
        details = (p.stderr or p.stdout or "").strip()
        return False, f"Az ffmpeg hibával tért vissza (kód={p.returncode}). {details}"
    return True, (p.stdout or "").splitlines()[0].strip()


def _ydl_common_opts(
    *,
    output_dir: Path,
    ffmpeg_dir: str | None,
    allow_playlist: bool,
    verbose: bool,
    outtmpl: str | None = None,
    progress_hooks: list | None = None,
) -> dict:
    opts = {
        "paths": {"home": str(output_dir)},
        "outtmpl": {"default": outtmpl or "%(title).200B [%(id)s].%(ext)s"},
        "windowsfilenames": True,
        "restrictfilenames": False,
        "noplaylist": not allow_playlist,
        "nopart": False,
        "overwrites": False,
        "ignoreerrors": False,
        "quiet": not verbose,
        "no_warnings": not verbose,
        "ffmpeg_location": ffmpeg_dir,
    }
    if progress_hooks:
        opts["progress_hooks"] = progress_hooks
    return opts


_WINDOWS_ILLEGAL_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1F\x7F]')
_WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def sanitize_windows_filename_base(name: str) -> str:
    base = _WINDOWS_ILLEGAL_CHARS.sub("_", name).strip()
    base = base.rstrip(". ")
    if not base:
        base = "audio"
    if base.upper() in _WINDOWS_RESERVED_NAMES:
        base = f"{base}_"
    if len(base) > 200:
        base = base[:200].rstrip(". ")
    return base


def download_audio(
    urls: list[str],
    *,
    output_dir: Path,
    ffmpeg_dir: str | None,
    audio_format: str,
    audio_quality: str,
    allow_playlist: bool,
    verbose: bool,
    name: str | None = None,
    progress_hooks: list | None = None,
) -> None:
    outtmpl = None
    if name:
        outtmpl = sanitize_windows_filename_base(name) + ".%(ext)s"
    opts = _ydl_common_opts(
        output_dir=output_dir,
        ffmpeg_dir=ffmpeg_dir,
        allow_playlist=allow_playlist,
        verbose=verbose,
        outtmpl=outtmpl,
        progress_hooks=progress_hooks,
    )
    opts.update(
        {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": audio_format,
                    "preferredquality": audio_quality,
                }
            ],
        }
    )
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download(urls)


def download_video(
    urls: list[str],
    *,
    output_dir: Path,
    ffmpeg_dir: str | None,
    container: str,
    allow_playlist: bool,
    verbose: bool,
    progress_hooks: list | None = None,
) -> None:
    opts = _ydl_common_opts(
        output_dir=output_dir,
        ffmpeg_dir=ffmpeg_dir,
        allow_playlist=allow_playlist,
        verbose=verbose,
        progress_hooks=progress_hooks,
    )
    opts.update(
        {
            "format": "bv*+ba/best",
            "merge_output_format": container,
        }
    )
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download(urls)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="letolto",
        description="YouTube letöltő (videó és hang kinyerés) yt-dlp + ffmpeg alapon.",
    )
    parser.add_argument(
        "urls",
        nargs="*",
        help="Egy vagy több URL. Ha üres, akkor bekéri interaktívan.",
    )
    parser.add_argument(
        "--mode",
        choices=["audio", "video"],
        default="audio",
        help="audio: hang kinyerés, video: videó letöltés/összefűzés",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=str(Path(__file__).resolve().parent / "downloads"),
        help="Kimeneti mappa (alapértelmezett: ./downloads)",
    )
    parser.add_argument(
        "--ffmpeg-dir",
        default=None,
        help=(
            "FFmpeg bin mappa. Ha nincs megadva: FFMPEG_DIR / YTDLP_FFMPEG_DIR env, "
            f"különben automatikusan: {DEFAULT_FFMPEG_DIR}"
        ),
    )
    parser.add_argument(
        "--playlist",
        action="store_true",
        help="Playlist letöltés engedélyezése (alapból noplaylist).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Részletesebb kimenet.",
    )

    audio = parser.add_argument_group("Audio")
    audio.add_argument(
        "--audio-format",
        default="mp3",
        choices=["mp3", "m4a", "opus", "wav", "flac"],
        help="Kimeneti hangformátum.",
    )
    audio.add_argument(
        "--audio-quality",
        default="192",
        help='Minőség (pl. "192" mp3-hoz).',
    )
    audio.add_argument(
        "--name",
        default=None,
        help="Hangfájl elnevezése (csak audio módban, 1 db URL-hez ajánlott).",
    )

    video = parser.add_argument_group("Video")
    video.add_argument(
        "--container",
        default="mp4",
        choices=["mp4", "mkv"],
        help="Végső konténer (merge_output_format).",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = _parse_args(argv)

    urls = list(args.urls)
    if not urls:
        url = input("Add meg a YouTube linket: ").strip()
        if not url:
            print("Nincs URL megadva.", file=sys.stderr)
            return 2
        urls = [url]

    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg_dir = _find_ffmpeg_dir(args.ffmpeg_dir)
    if ffmpeg_dir:
        ok, msg = _check_ffmpeg(ffmpeg_dir)
        if not ok:
            print(f"FFmpeg ellenőrzés sikertelen: {msg}", file=sys.stderr)
            print(
                "Tipp: próbáld meg hivatalos forrásból telepíteni (pl. winget/choco), "
                "vagy Windows-ban a fájl Tulajdonságoknál 'Feloldás' (Unblock), ha internetes letöltés miatt blokkolt.",
                file=sys.stderr,
            )
            return 3
        if args.verbose:
            print(f"FFmpeg OK: {msg}")
    else:
        print(
            "Figyelem: nem találtam FFmpeg-et. Videó összefűzéshez és hang kinyeréshez szükséges.",
            file=sys.stderr,
        )
        print(
            f"Add meg: --ffmpeg-dir \"{DEFAULT_FFMPEG_DIR}\" vagy állítsd be az FFMPEG_DIR env változót.",
            file=sys.stderr,
        )
        return 3

    if args.mode == "audio":
        if args.name and len(urls) != 1:
            print("--name használatához adj meg pontosan 1 URL-t.", file=sys.stderr)
            return 2
        download_audio(
            urls,
            output_dir=output_dir,
            ffmpeg_dir=ffmpeg_dir,
            audio_format=args.audio_format,
            audio_quality=args.audio_quality,
            allow_playlist=args.playlist,
            verbose=args.verbose,
            name=args.name,
        )
        print(f"Kész! Hangfájl(ok) itt: {output_dir}")
        return 0

    download_video(
        urls,
        output_dir=output_dir,
        ffmpeg_dir=ffmpeg_dir,
        container=args.container,
        allow_playlist=args.playlist,
        verbose=args.verbose,
    )
    print(f"Kész! Videó(k) itt: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
