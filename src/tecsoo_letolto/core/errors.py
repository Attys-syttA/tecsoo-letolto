from __future__ import annotations


class TecsoLetoltoError(Exception):
    category = "unknown"
    default_user_message = "Ismeretlen hiba történt."

    def __init__(
        self,
        user_message: str | None = None,
        *,
        technical_detail: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        self.user_message = user_message or self.default_user_message
        self.technical_detail = technical_detail
        self.cause = cause
        super().__init__(self.user_message)


class InvalidUrlError(TecsoLetoltoError):
    category = "invalid_url"
    default_user_message = "A megadott link üres vagy hibás."


class UnsupportedUrlError(TecsoLetoltoError):
    category = "unsupported_url"
    default_user_message = "A megadott linket a letöltő nem támogatja."


class NetworkError(TecsoLetoltoError):
    category = "network"
    default_user_message = "Nem sikerült kapcsolódni az internethez vagy a tartalom szolgáltatójához."


class RestrictedContentError(TecsoLetoltoError):
    category = "restricted_content"
    default_user_message = "A tartalom nem érhető el, vagy korlátozott hozzáférésű."


class DownloadCancelledError(TecsoLetoltoError):
    category = "download_cancelled"
    default_user_message = "A letöltés megszakadt."


class OutputDirectoryError(TecsoLetoltoError):
    category = "output_directory"
    default_user_message = "A mentési mappa nem használható."


class NotEnoughSpaceError(TecsoLetoltoError):
    category = "not_enough_space"
    default_user_message = "Nincs elég szabad tárhely a mentéshez."


class FfmpegError(TecsoLetoltoError):
    category = "ffmpeg"
    default_user_message = "Az FFmpeg feldolgozás hibára futott."


class YtDlpError(TecsoLetoltoError):
    category = "ytdlp"
    default_user_message = "A letöltő komponens hibára futott."


class ToolMissingError(TecsoLetoltoError):
    category = "tool_missing"
    default_user_message = "Hiányzik egy szükséges programkomponens."


class ToolUpdateError(TecsoLetoltoError):
    category = "tool_update"
    default_user_message = "Nem sikerült frissíteni a letöltő komponenst."


class FilenameConflictError(TecsoLetoltoError):
    category = "filename_conflict"
    default_user_message = "Nem sikerült szabad fájlnevet találni."
