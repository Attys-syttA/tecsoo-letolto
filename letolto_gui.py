from __future__ import annotations

import threading
import traceback
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import letolto


@dataclass
class UiState:
    running: bool = False


class TkLogger:
    def __init__(self, append_line):
        self._append_line = append_line

    def debug(self, msg):
        if msg:
            self._append_line(str(msg))

    def warning(self, msg):
        if msg:
            self._append_line(f"[WARN] {msg}")

    def error(self, msg):
        if msg:
            self._append_line(f"[ERROR] {msg}")


def main() -> int:
    root = tk.Tk()
    root.title("tecsoo-letolto – YouTube letöltő")
    root.geometry("820x560")

    state = UiState()

    url_var = tk.StringVar()
    output_var = tk.StringVar(value=str(letolto.default_download_dir()))
    mode_var = tk.StringVar(value="audio")
    playlist_var = tk.BooleanVar(value=False)
    verbose_var = tk.BooleanVar(value=False)

    ffmpeg_var = tk.StringVar(value=(letolto._find_ffmpeg_dir(None) or ""))

    audio_format_var = tk.StringVar(value="mp3")
    audio_quality_var = tk.StringVar(value="192")
    audio_name_var = tk.StringVar(value="")

    container_var = tk.StringVar(value="mp4")

    def set_running(r: bool) -> None:
        state.running = r
        start_btn.configure(state=("disabled" if r else "normal"))
        for w in (url_entry, output_entry, ffmpeg_entry):
            w.configure(state=("disabled" if r else "normal"))
        for w in (
            browse_out_btn,
            browse_ffmpeg_btn,
            test_ffmpeg_btn,
            mode_audio_rb,
            mode_video_rb,
            playlist_cb,
            verbose_cb,
            audio_format_om,
            audio_quality_entry,
            audio_name_entry,
            container_om,
        ):
            w.configure(state=("disabled" if r else "normal"))
        if not r:
            on_mode_change()

    def append_line(line: str) -> None:
        log.configure(state="normal")
        log.insert("end", line + "\n")
        log.see("end")
        log.configure(state="disabled")

    def ui_append(line: str) -> None:
        root.after(0, append_line, line)

    def ui_set_status(text: str) -> None:
        root.after(0, status_var.set, text)

    def browse_output() -> None:
        p = filedialog.askdirectory(title="Válaszd ki a célmappát")
        if p:
            output_var.set(p)

    def browse_ffmpeg() -> None:
        p = filedialog.askdirectory(title="Válaszd ki az FFmpeg bin mappát (ffmpeg.exe)")
        if p:
            ffmpeg_var.set(p)

    def test_ffmpeg() -> None:
        ffdir = ffmpeg_var.get().strip()
        ffdir = letolto._find_ffmpeg_dir(ffdir or None)
        if not ffdir:
            messagebox.showerror("FFmpeg", "Nem találtam FFmpeg-et. Add meg a bin mappát (ahol az ffmpeg.exe van).")
            return
        ok, msg = letolto._check_ffmpeg(ffdir)
        if ok:
            messagebox.showinfo("FFmpeg", f"OK: {msg}\n\nHasználva: {ffdir}")
        else:
            messagebox.showerror("FFmpeg", msg)

    def on_mode_change(*_args) -> None:
        is_audio = mode_var.get() == "audio"

        def set_state(widgets, enabled: bool) -> None:
            s = "normal" if enabled else "disabled"
            for w in widgets:
                try:
                    w.configure(state=s)
                except tk.TclError:
                    pass

        set_state(
            [audio_format_om, audio_quality_entry, audio_name_entry],
            enabled=is_audio and (not state.running),
        )
        set_state([container_om], enabled=(not is_audio) and (not state.running))

    def start_download() -> None:
        if state.running:
            return
        url = url_var.get().strip()
        if not url:
            messagebox.showerror("Hiba", "Add meg a YouTube linket.")
            return

        output_dir = Path(output_var.get().strip() or ".").expanduser().resolve()
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Hiba", f"Nem tudtam létrehozni a célmappát:\n{e}")
            return

        ffmpeg_dir = ffmpeg_var.get().strip()
        ffmpeg_dir = letolto._find_ffmpeg_dir(ffmpeg_dir or None)
        if not ffmpeg_dir:
            messagebox.showerror(
                "FFmpeg hiányzik",
                "Nem találtam FFmpeg-et.\nAdd meg a bin mappát (ahol az ffmpeg.exe van), vagy állítsd be az FFMPEG_DIR env-et.",
            )
            return

        ok, msg = letolto._check_ffmpeg(ffmpeg_dir)
        if not ok:
            messagebox.showerror("FFmpeg", f"FFmpeg ellenőrzés sikertelen:\n{msg}")
            return

        if not ffmpeg_var.get().strip():
            ffmpeg_var.set(ffmpeg_dir)

        logger = TkLogger(ui_append)

        def progress_hook(d: dict) -> None:
            status = d.get("status")
            if status == "downloading":
                pct = d.get("_percent_str") or ""
                speed = d.get("_speed_str") or ""
                eta = d.get("_eta_str") or ""
                ui_set_status(f"Letöltés… {pct} {speed} ETA {eta}".strip())
            elif status == "finished":
                ui_set_status("Letöltés kész, feldolgozás…")
            elif status == "error":
                ui_set_status("Hiba történt.")

        def worker() -> None:
            try:
                ui_append(f"FFmpeg: {msg}")
                ui_append(f"Célmappa: {output_dir}")
                ui_set_status("Indítás…")

                if mode_var.get() == "audio":
                    name = audio_name_var.get().strip() or None
                    letolto.download_audio(
                        [url],
                        output_dir=output_dir,
                        ffmpeg_dir=ffmpeg_dir,
                        audio_format=audio_format_var.get().strip(),
                        audio_quality=audio_quality_var.get().strip(),
                        allow_playlist=bool(playlist_var.get()),
                        verbose=bool(verbose_var.get()),
                        name=name,
                        progress_hooks=[progress_hook],
                    )
                else:
                    letolto.download_video(
                        [url],
                        output_dir=output_dir,
                        ffmpeg_dir=ffmpeg_dir,
                        container=container_var.get().strip(),
                        allow_playlist=bool(playlist_var.get()),
                        verbose=bool(verbose_var.get()),
                        progress_hooks=[progress_hook],
                    )
                ui_set_status("Kész.")
                ui_append("Kész.")
            except Exception as e:
                ui_set_status("Hiba.")
                logger.error(e)
            finally:
                root.after(0, set_running, False)

        set_running(True)
        threading.Thread(target=worker, daemon=True).start()

    # Layout
    pad = {"padx": 10, "pady": 6}

    top = ttk.Frame(root)
    top.pack(fill="x")

    ttk.Label(top, text="YouTube link:").grid(row=0, column=0, sticky="w", **pad)
    url_entry = ttk.Entry(top, textvariable=url_var)
    url_entry.grid(row=0, column=1, sticky="ew", **pad)

    ttk.Label(top, text="Célmappa:").grid(row=1, column=0, sticky="w", **pad)
    output_entry = ttk.Entry(top, textvariable=output_var)
    output_entry.grid(row=1, column=1, sticky="ew", **pad)
    browse_out_btn = ttk.Button(top, text="Tallózás…", command=browse_output)
    browse_out_btn.grid(row=1, column=2, sticky="ew", **pad)

    ttk.Label(top, text="FFmpeg bin mappa:").grid(row=2, column=0, sticky="w", **pad)
    ffmpeg_entry = ttk.Entry(top, textvariable=ffmpeg_var)
    ffmpeg_entry.grid(row=2, column=1, sticky="ew", **pad)
    browse_ffmpeg_btn = ttk.Button(top, text="Tallózás…", command=browse_ffmpeg)
    browse_ffmpeg_btn.grid(row=2, column=2, sticky="ew", **pad)
    test_ffmpeg_btn = ttk.Button(top, text="FFmpeg teszt", command=test_ffmpeg)
    test_ffmpeg_btn.grid(row=2, column=3, sticky="ew", **pad)

    modes = ttk.Frame(root)
    modes.pack(fill="x")
    ttk.Label(modes, text="Mód:").pack(side="left", padx=10, pady=6)
    mode_audio_rb = ttk.Radiobutton(modes, text="Hang (audio)", variable=mode_var, value="audio", command=on_mode_change)
    mode_video_rb = ttk.Radiobutton(modes, text="Videó (video)", variable=mode_var, value="video", command=on_mode_change)
    mode_audio_rb.pack(side="left", padx=6)
    mode_video_rb.pack(side="left", padx=6)

    playlist_cb = ttk.Checkbutton(modes, text="Playlist engedélyezése", variable=playlist_var)
    playlist_cb.pack(side="left", padx=18)
    verbose_cb = ttk.Checkbutton(modes, text="Verbose", variable=verbose_var)
    verbose_cb.pack(side="left")

    opts = ttk.Frame(root)
    opts.pack(fill="x")

    audio_frame = ttk.LabelFrame(opts, text="Audio beállítások")
    audio_frame.pack(side="left", fill="both", expand=True, padx=10, pady=6)

    ttk.Label(audio_frame, text="Formátum:").grid(row=0, column=0, sticky="w", **pad)
    audio_format_om = ttk.OptionMenu(audio_frame, audio_format_var, audio_format_var.get(), "mp3", "m4a", "opus", "wav", "flac")
    audio_format_om.grid(row=0, column=1, sticky="ew", **pad)

    ttk.Label(audio_frame, text="Minőség:").grid(row=1, column=0, sticky="w", **pad)
    audio_quality_entry = ttk.Entry(audio_frame, textvariable=audio_quality_var)
    audio_quality_entry.grid(row=1, column=1, sticky="ew", **pad)

    ttk.Label(audio_frame, text="Név (opcionális):").grid(row=2, column=0, sticky="w", **pad)
    audio_name_entry = ttk.Entry(audio_frame, textvariable=audio_name_var)
    audio_name_entry.grid(row=2, column=1, sticky="ew", **pad)

    audio_frame.columnconfigure(1, weight=1)

    video_frame = ttk.LabelFrame(opts, text="Video beállítások")
    video_frame.pack(side="left", fill="both", expand=True, padx=10, pady=6)

    ttk.Label(video_frame, text="Konténer:").grid(row=0, column=0, sticky="w", **pad)
    container_om = ttk.OptionMenu(video_frame, container_var, container_var.get(), "mp4", "mkv")
    container_om.grid(row=0, column=1, sticky="ew", **pad)
    video_frame.columnconfigure(1, weight=1)

    actions = ttk.Frame(root)
    actions.pack(fill="x")
    start_btn = ttk.Button(actions, text="Letöltés indítása", command=start_download)
    start_btn.pack(side="left", padx=10, pady=6)

    status_var = tk.StringVar(value="Készen áll.")
    status_lbl = ttk.Label(actions, textvariable=status_var)
    status_lbl.pack(side="left", padx=10)

    log = tk.Text(root, height=12, wrap="word")
    log.pack(fill="both", expand=True, padx=10, pady=10)
    log.configure(state="disabled")

    top.columnconfigure(1, weight=1)

    on_mode_change()
    root.mainloop()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        log_path = Path(__file__).resolve().with_name("gui_error.log")
        try:
            log_path.write_text(traceback.format_exc(), encoding="utf-8")
        except Exception:
            pass
        try:
            messagebox.showerror(
                "Indítási hiba",
                f"A GUI nem tudott elindulni.\nRészletek: {log_path}",
            )
        except Exception:
            pass
        raise
