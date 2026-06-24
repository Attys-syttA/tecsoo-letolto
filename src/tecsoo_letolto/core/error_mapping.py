from __future__ import annotations

from .errors import (
    FfmpegError,
    NetworkError,
    NotEnoughSpaceError,
    OutputDirectoryError,
    RestrictedContentError,
    TecsoLetoltoError,
    UnsupportedUrlError,
    YtDlpError,
)


def _combined_text(*parts: str) -> str:
    return "\n".join(part for part in parts if part).lower()


def map_subprocess_failure(tool: str, returncode: int, stdout: str, stderr: str) -> TecsoLetoltoError:
    text = _combined_text(stdout, stderr)
    detail = (stderr or stdout or "").strip() or f"{tool} exited with code {returncode}"

    if "unsupported url" in text or "no suitable extractor" in text:
        return UnsupportedUrlError(technical_detail=detail)

    if any(marker in text for marker in ("private video", "sign in", "age-restricted", "members-only")):
        return RestrictedContentError(technical_detail=detail)

    if any(marker in text for marker in ("timed out", "timeout", "temporary failure", "name resolution", "network is unreachable")):
        return NetworkError(technical_detail=detail)

    if any(marker in text for marker in ("permission denied", "access is denied", "winerror 5")):
        return OutputDirectoryError(technical_detail=detail)

    if any(marker in text for marker in ("no space left", "not enough space", "disk full")):
        return NotEnoughSpaceError(technical_detail=detail)

    if tool.lower().startswith("ffmpeg"):
        return FfmpegError(technical_detail=detail)

    return YtDlpError(technical_detail=detail)


def map_exception(exc: Exception) -> TecsoLetoltoError:
    if isinstance(exc, TecsoLetoltoError):
        return exc
    if isinstance(exc, PermissionError):
        return OutputDirectoryError(technical_detail=str(exc), cause=exc)
    if isinstance(exc, OSError):
        text = str(exc).lower()
        if "no space" in text or "disk full" in text:
            return NotEnoughSpaceError(technical_detail=str(exc), cause=exc)
    return TecsoLetoltoError(technical_detail=str(exc), cause=exc)


def user_error_text(error: TecsoLetoltoError) -> str:
    suggestions = {
        "invalid_url": [
            "Ellenőrizd, hogy a linket teljes egészében másoltad-e be.",
            "A linknek http:// vagy https:// kezdetűnek kell lennie.",
        ],
        "unsupported_url": [
            "Nyisd meg a linket böngészőben, és ellenőrizd, hogy valódi médiaoldal-e.",
            "Próbáld meg később frissíteni a letöltő komponenst.",
        ],
        "network": [
            "Ellenőrizd az internetkapcsolatot.",
            "Próbáld meg később újra.",
        ],
        "restricted_content": [
            "Ellenőrizd, hogy a tartalom nyilvánosan elérhető-e.",
            "A program nem kezel bejelentkezést, cookie-t vagy korlátozás-megkerülést.",
        ],
        "output_directory": [
            "Válassz másik mentési mappát.",
            "Ellenőrizd, hogy van-e írási jogosultságod a mappához.",
        ],
        "not_enough_space": [
            "Szabadíts fel tárhelyet, vagy válassz másik meghajtót.",
        ],
        "ffmpeg": [
            "Ellenőrizd, hogy a portable csomagban megvan-e az FFmpeg.",
            "Futtasd a későbbi self-check ellenőrzést.",
        ],
        "ytdlp": [
            "Ellenőrizd, hogy a link böngészőben megnyitható-e.",
            "Próbáld meg frissíteni a letöltő komponenst.",
        ],
    }
    lines = [
        "Nem sikerült végrehajtani a műveletet.",
        "",
        "Valószínű ok:",
        error.user_message,
    ]
    category_suggestions = suggestions.get(error.category)
    if category_suggestions:
        lines.extend(["", "Mit próbálhatsz meg:"])
        lines.extend(f"- {item}" for item in category_suggestions)
    return "\n".join(lines)
