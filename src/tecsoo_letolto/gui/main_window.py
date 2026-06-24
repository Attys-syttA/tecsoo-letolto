from __future__ import annotations

import tkinter as tk
import threading
import tempfile
from datetime import datetime
from pathlib import Path
from tkinter import scrolledtext
from tkinter import filedialog, messagebox, ttk

from tecsoo_letolto.core.download_manager import DownloadManager
from tecsoo_letolto.core.error_mapping import map_exception, user_error_text
from tecsoo_letolto.core.paths import default_output_dir, ensure_writable_dir, logs_dir
from tecsoo_letolto.core.progress import CancelToken, ProgressEvent
from tecsoo_letolto.core.support_report import (
    SupportContext,
    build_support_report,
    current_windows_version,
    tail_log_lines,
)
from tecsoo_letolto.gui.help_text import HELP_TEXT
from tecsoo_letolto.gui.tray import WindowsTrayIcon
from tecsoo_letolto.gui.view_model import DownloadFormState, to_download_request, validate_form
from tecsoo_letolto.services.ffmpeg_service import find_packaged_ffmpeg
from tecsoo_letolto.services.update_service import get_latest_ytdlp_version, install_latest_ytdlp
from tecsoo_letolto.services.ytdlp_service import YtDlpTool, find_packaged_ytdlp
from tecsoo_letolto.version import __version__


class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("TecsoLetolto")
        self.root.geometry("860x520")
        self.root.minsize(760, 460)

        self.url_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.filename_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="audio")
        self.audio_format_var = tk.StringVar(value="mp3")
        self.video_format_var = tk.StringVar(value="mp4")
        self.quality_var = tk.StringVar(value="good")
        self.status_var = tk.StringVar(value="Készen áll.")
        self.progress_var = tk.DoubleVar(value=0)
        self.last_error_summary: str | None = None
        self.running = False
        self.cancel_token: CancelToken | None = None
        self.tray_icon: WindowsTrayIcon | None = None
        self.tray_poll_after_id: str | None = None

        self._build()
        self._sync_mode_controls()
        self.root.protocol("WM_DELETE_WINDOW", self._close)

    def run(self) -> None:
        self.root.mainloop()

    def _build(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main = ttk.Frame(self.root, padding=14)
        main.grid(row=0, column=0, sticky="nsew")
        main.columnconfigure(1, weight=1)
        main.rowconfigure(7, weight=1)

        ttk.Label(main, text="Link").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=6)
        ttk.Entry(main, textvariable=self.url_var).grid(row=0, column=1, sticky="ew", pady=6)
        ttk.Button(main, text="Beillesztés", command=self._paste_url).grid(row=0, column=2, sticky="ew", padx=(10, 0), pady=6)

        ttk.Label(main, text="Mentési mappa").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=6)
        ttk.Entry(main, textvariable=self.output_dir_var).grid(row=1, column=1, sticky="ew", pady=6)
        ttk.Button(main, text="Tallózás", command=self._browse_output_dir).grid(row=1, column=2, sticky="ew", padx=(10, 0), pady=6)

        ttk.Label(main, text="Fájlnév").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=6)
        ttk.Entry(main, textvariable=self.filename_var).grid(row=2, column=1, sticky="ew", pady=6)
        ttk.Button(main, text="Mezők törlése", command=self._clear_fields).grid(row=2, column=2, sticky="ew", padx=(10, 0), pady=6)

        mode_frame = ttk.LabelFrame(main, text="Letöltési mód", padding=8)
        mode_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(8, 6))
        ttk.Radiobutton(mode_frame, text="Csak hang", variable=self.mode_var, value="audio", command=self._sync_mode_controls).pack(side="left", padx=(0, 14))
        ttk.Radiobutton(mode_frame, text="Videó + hang", variable=self.mode_var, value="video", command=self._sync_mode_controls).pack(side="left")

        options = ttk.Frame(main)
        options.grid(row=4, column=0, columnspan=3, sticky="ew", pady=6)
        for index in range(6):
            options.columnconfigure(index, weight=1)

        ttk.Label(options, text="Hangformátum").grid(row=0, column=0, sticky="w")
        self.audio_format_combo = ttk.Combobox(
            options,
            textvariable=self.audio_format_var,
            values=("mp3", "m4a", "opus", "wav"),
            state="readonly",
            width=10,
        )
        self.audio_format_combo.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        ttk.Label(options, text="Videóformátum").grid(row=0, column=1, sticky="w")
        self.video_format_combo = ttk.Combobox(
            options,
            textvariable=self.video_format_var,
            values=("mp4", "mkv"),
            state="readonly",
            width=10,
        )
        self.video_format_combo.grid(row=1, column=1, sticky="ew", padx=(0, 10))

        ttk.Label(options, text="Minőség").grid(row=0, column=2, sticky="w")
        self.quality_combo = ttk.Combobox(
            options,
            textvariable=self.quality_var,
            values=("normal", "good", "best"),
            state="readonly",
            width=16,
        )
        self.quality_combo.grid(row=1, column=2, sticky="ew")

        actions = ttk.Frame(main)
        actions.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(12, 6))
        self.start_button = ttk.Button(actions, text="Letöltés indítása", command=self._start_download)
        self.start_button.pack(side="left", padx=(0, 8), pady=3)
        self.cancel_button = ttk.Button(actions, text="Letöltés megszakítása", command=self._cancel_download, state="disabled")
        self.cancel_button.pack(side="left", padx=(0, 8), pady=3)
        for label, command in (
            ("Mappa megnyitása", self._open_output_dir),
            ("Értesítési területre", self._minimize_to_tray),
            ("Frissítés ellenőrzése", self._check_ytdlp_update),
            ("Súgó", self._show_help),
            ("Support", self._show_support),
            ("Névjegy", self._show_about),
            ("Kilépés", self.root.destroy),
        ):
            ttk.Button(actions, text=label, command=command).pack(side="left", padx=(0, 8), pady=3)

        ttk.Label(main, textvariable=self.status_var).grid(row=6, column=0, columnspan=3, sticky="w", pady=(12, 4))
        ttk.Progressbar(main, variable=self.progress_var, maximum=100).grid(row=7, column=0, columnspan=3, sticky="ew", pady=(0, 6))

    def _form_state(self) -> DownloadFormState:
        return DownloadFormState(
            url=self.url_var.get(),
            output_dir=self.output_dir_var.get(),
            filename=self.filename_var.get(),
            mode=self.mode_var.get(),
            audio_format=self.audio_format_var.get(),
            video_format=self.video_format_var.get(),
            quality=self.quality_var.get(),
        )

    def _sync_mode_controls(self) -> None:
        if not hasattr(self, "audio_format_combo"):
            return
        if self.mode_var.get() == "audio":
            self.audio_format_combo.configure(state="readonly")
            self.video_format_combo.configure(state="disabled")
        else:
            self.audio_format_combo.configure(state="disabled")
            self.video_format_combo.configure(state="readonly")

    def _paste_url(self) -> None:
        try:
            self.url_var.set(self.root.clipboard_get().strip())
        except tk.TclError:
            self.status_var.set("A vágólap üres.")

    def _browse_output_dir(self) -> None:
        selected = filedialog.askdirectory(title="Mentési mappa kiválasztása")
        if selected:
            self.output_dir_var.set(selected)

    def _clear_fields(self) -> None:
        self.url_var.set("")
        self.filename_var.set("")
        self.status_var.set("Készen áll.")
        self.progress_var.set(0)

    def _start_download(self) -> None:
        if self.running:
            return
        errors = validate_form(self._form_state())
        if errors:
            self.last_error_summary = "\n".join(errors)
            messagebox.showerror("Hiba", self.last_error_summary)
            self.status_var.set("Hiba történt.")
            return
        request = to_download_request(self._form_state())
        self.cancel_token = CancelToken()
        self._set_running(True)
        self.status_var.set("Letöltés előkészítése...")

        class GuiProgressSink:
            def __init__(self, window: MainWindow) -> None:
                self._window = window

            def publish(self, event: ProgressEvent) -> None:
                self._window.root.after(0, self._window._apply_progress_event, event)

        progress_sink = GuiProgressSink(self)

        def worker() -> None:
            try:
                result = DownloadManager().run(
                    request,
                    progress_sink=progress_sink,
                    cancel_token=self.cancel_token,
                )
            except Exception as exc:
                error = map_exception(exc)
                self.last_error_summary = error.user_message
                self.root.after(0, self._download_failed, user_error_text(error))
                return
            self.root.after(0, self._download_finished, result.output_path)

        threading.Thread(target=worker, daemon=True).start()

    def _cancel_download(self) -> None:
        if self.running:
            if self.cancel_token:
                self.cancel_token.cancel()
            self.status_var.set("Megszakítás előkészítése...")
            return
        self.status_var.set("Nincs futó letöltés.")

    def _set_running(self, running: bool) -> None:
        self.running = running
        self.start_button.configure(state="disabled" if running else "normal")
        self.cancel_button.configure(state="normal" if running else "disabled")

    def _download_failed(self, message: str) -> None:
        self._set_running(False)
        self.cancel_token = None
        self.status_var.set("Hiba történt.")
        messagebox.showerror("Hiba", message)

    def _download_finished(self, output_path: Path) -> None:
        self._set_running(False)
        self.cancel_token = None
        self.progress_var.set(100)
        self.status_var.set("Kész.")
        messagebox.showinfo("Kész", f"A letöltés elkészült:\n{output_path}")

    def _apply_progress_event(self, event: ProgressEvent) -> None:
        if event.percent is not None:
            self.progress_var.set(max(0, min(100, event.percent)))
        self.status_var.set(event.message)

    def _open_output_dir(self) -> None:
        output_dir = self.output_dir_var.get().strip()
        if not output_dir:
            messagebox.showinfo("Mappa", "Nincs még mentési mappa megadva.")
            return
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            import os

            os.startfile(output_dir)  # type: ignore[attr-defined]
        except Exception as exc:
            self.last_error_summary = str(exc)
            messagebox.showerror("Mappa megnyitása", str(exc))

    def _show_help(self) -> None:
        self._show_text_window("Súgó", HELP_TEXT)

    def _check_ytdlp_update(self) -> None:
        if self.running:
            self.status_var.set("Futó letöltés közben nem lehet frissítést ellenőrizni.")
            return
        self.status_var.set("yt-dlp frissítés ellenőrzése...")

        def worker() -> None:
            try:
                tool = find_packaged_ytdlp()
                latest = get_latest_ytdlp_version()
            except Exception as exc:
                error = map_exception(exc)
                self.last_error_summary = error.user_message
                self.root.after(0, self._show_update_error, user_error_text(error))
                return
            self.root.after(0, self._confirm_ytdlp_update, tool, latest)

        threading.Thread(target=worker, daemon=True).start()

    def _confirm_ytdlp_update(self, tool: YtDlpTool, latest_version: str) -> None:
        current_version = tool.version.strip()
        if current_version == latest_version:
            self.status_var.set("A yt-dlp naprakész.")
            messagebox.showinfo("yt-dlp frissítés", f"A jelenlegi yt-dlp verzió naprakész:\n{current_version}")
            return
        approved = messagebox.askyesno(
            "yt-dlp frissítés",
            f"Jelenlegi verzió: {current_version}\nElérhető verzió: {latest_version}\n\nFrissíted a beépített yt-dlp.exe fájlt?",
        )
        if not approved:
            self.status_var.set("yt-dlp frissítés kihagyva.")
            return
        self.status_var.set("yt-dlp frissítése...")

        def worker() -> None:
            try:
                with tempfile.TemporaryDirectory(prefix="tecsoletolto-ytdlp-") as temp_dir:
                    result = install_latest_ytdlp(
                        tool.executable,
                        Path(temp_dir),
                        previous_version=current_version,
                    )
            except Exception as exc:
                error = map_exception(exc)
                self.last_error_summary = error.user_message
                self.root.after(0, self._show_update_error, user_error_text(error))
                return
            self.root.after(0, self._show_update_success, result.current_version)

        threading.Thread(target=worker, daemon=True).start()

    def _show_update_error(self, message: str) -> None:
        self.status_var.set("yt-dlp frissítés sikertelen.")
        messagebox.showerror("yt-dlp frissítés", message)

    def _show_update_success(self, version: str) -> None:
        self.status_var.set("yt-dlp frissítve.")
        messagebox.showinfo("yt-dlp frissítés", f"A yt-dlp frissítése elkészült:\n{version}")

    def _show_support(self) -> None:
        output_dir = Path(self.output_dir_var.get().strip()) if self.output_dir_var.get().strip() else default_output_dir()
        output_writable = None
        try:
            ensure_writable_dir(output_dir)
            output_writable = True
        except Exception:
            output_writable = False
        try:
            ytdlp_version = find_packaged_ytdlp().version
        except Exception:
            ytdlp_version = None
        try:
            ffmpeg_version = find_packaged_ffmpeg().version
        except Exception:
            ffmpeg_version = None
        log_files = sorted(logs_dir().glob("*.log")) if logs_dir().is_dir() else []
        log_lines = tail_log_lines(log_files[-1], max_lines=40) if log_files else []
        context = SupportContext(
            app_version=__version__,
            windows_version=current_windows_version(),
            ytdlp_version=ytdlp_version,
            ffmpeg_version=ffmpeg_version,
            last_error_category=None,
            last_error_summary=self.last_error_summary,
            output_dir_writable=output_writable,
            mode=self.mode_var.get(),
            timestamp=datetime.now(),
            url=self.url_var.get(),
        )
        report = build_support_report(context, log_lines)
        self._show_text_window("Support jelentés előnézet", report)

    def _show_about(self) -> None:
        messagebox.showinfo("Névjegy", f"TecsoLetolto\nVerzió: {__version__}")

    def _show_text_window(self, title: str, text: str) -> None:
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("760x560")
        window.minsize(560, 360)
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        box = scrolledtext.ScrolledText(window, wrap="word", padx=12, pady=12)
        box.grid(row=0, column=0, sticky="nsew")
        box.insert("1.0", text)
        box.configure(state="disabled")
        ttk.Button(window, text="Bezárás", command=window.destroy).grid(row=1, column=0, sticky="e", padx=12, pady=10)

    def _minimize_to_tray(self) -> None:
        self.root.update_idletasks()
        hwnd = self.root.winfo_id()
        if self.tray_icon is None:
            self.tray_icon = WindowsTrayIcon(hwnd, "TecsoLetolto")
        if self.tray_icon.show():
            self.root.withdraw()
            self.status_var.set("Az alkalmazás az értesítési területen fut.")
            self._start_tray_restore_polling()
        else:
            self.root.iconify()
            self.status_var.set("Az alkalmazás minimalizálva.")

    def _start_tray_restore_polling(self) -> None:
        if self.tray_poll_after_id is None:
            self.tray_poll_after_id = self.root.after(200, self._poll_tray_restore)

    def _stop_tray_restore_polling(self) -> None:
        if self.tray_poll_after_id is not None:
            self.root.after_cancel(self.tray_poll_after_id)
            self.tray_poll_after_id = None

    def _poll_tray_restore(self) -> None:
        self.tray_poll_after_id = None
        if not self.tray_icon or not self.tray_icon.active:
            return
        if self.tray_icon.consume_restore_request():
            self._restore_from_tray()
            return
        self._start_tray_restore_polling()

    def _restore_from_tray(self) -> None:
        self._stop_tray_restore_polling()
        if self.tray_icon:
            self.tray_icon.remove()
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def _close(self) -> None:
        self._stop_tray_restore_polling()
        if self.tray_icon:
            self.tray_icon.remove()
        self.root.destroy()


def run_gui() -> int:
    MainWindow().run()
    return 0
