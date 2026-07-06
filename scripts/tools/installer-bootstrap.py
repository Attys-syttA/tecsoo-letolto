from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


APP_NAME = "TecsoLetolto"
DESKTOP_SHORTCUT_NAME = f"{APP_NAME}.lnk"
DEFAULT_DESTINATION = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "Programs" / APP_NAME


def bundled_path(name: str) -> Path:
    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base_dir / name


def read_version() -> str:
    payload = bundled_path("payload.zip")
    try:
        with zipfile.ZipFile(payload) as archive:
            with archive.open(f"{APP_NAME}/VERSION.txt") as handle:
                return handle.read().decode("utf-8").strip()
    except Exception:
        return "ismeretlen"


def create_desktop_shortcut(target_exe: Path) -> None:
    desktop_dir = Path(os.environ["USERPROFILE"]) / "Desktop"
    shortcut_path = desktop_dir / DESKTOP_SHORTCUT_NAME
    script = f"""
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
$Shortcut.TargetPath = '{target_exe}'
$Shortcut.WorkingDirectory = '{target_exe.parent}'
$Shortcut.IconLocation = '{target_exe},0'
$Shortcut.Save()
"""
    subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def extract_payload(staging_dir: Path) -> Path:
    payload_zip = bundled_path("payload.zip")
    extract_root = staging_dir / "payload"
    with zipfile.ZipFile(payload_zip) as archive:
        archive.extractall(extract_root)
    return extract_root / APP_NAME


class InstallerWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} telepito")
        self.root.geometry("560x260")
        self.root.resizable(False, False)

        self.destination_var = tk.StringVar(value=str(DEFAULT_DESTINATION))
        self.shortcut_var = tk.BooleanVar(value=True)
        self.launch_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value=f"Telepitesre kesz. Verzió: {read_version()}")

        self._build()

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        ttk.Label(
            frame,
            text="A telepito a friss TecsoLetolto verziot masolja a valasztott mappaba.",
            wraplength=500,
            justify="left",
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 14))

        ttk.Label(frame, text="Celmappa").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=6)
        ttk.Entry(frame, textvariable=self.destination_var).grid(row=1, column=1, sticky="ew", pady=6)
        ttk.Button(frame, text="Tallozas", command=self._browse).grid(row=1, column=2, sticky="ew", pady=6)

        ttk.Checkbutton(frame, text="Asztali parancsikon letrehozasa", variable=self.shortcut_var).grid(
            row=2, column=0, columnspan=3, sticky="w", pady=(10, 4)
        )
        ttk.Checkbutton(frame, text="Program inditasa telepites utan", variable=self.launch_var).grid(
            row=3, column=0, columnspan=3, sticky="w", pady=(0, 10)
        )

        ttk.Label(frame, textvariable=self.status_var, wraplength=500, justify="left").grid(
            row=4, column=0, columnspan=3, sticky="w", pady=(0, 12)
        )

        actions = ttk.Frame(frame)
        actions.grid(row=5, column=0, columnspan=3, sticky="e")
        ttk.Button(actions, text="Kilepes", command=self.root.destroy).pack(side="right")
        ttk.Button(actions, text="Telepites", command=self._install).pack(side="right", padx=(0, 8))

    def _browse(self) -> None:
        selected = filedialog.askdirectory(title="Telepitesi mappa kivalasztasa")
        if selected:
            self.destination_var.set(selected)

    def _install(self) -> None:
        destination = Path(self.destination_var.get().strip()).expanduser()
        if not self.destination_var.get().strip():
            messagebox.showerror("Hiba", "Adj meg egy telepitesi mappat.")
            return

        if destination.exists() and any(destination.iterdir()):
            answer = messagebox.askyesno(
                "Feluliras",
                "A celmappa mar tartalmaz fajlokat. A telepito felulirja a korabbi TecsoLetolto verziot. Folytatod?",
            )
            if not answer:
                return

        staging_root = Path(tempfile.mkdtemp(prefix="tecso-installer-"))
        backup_dir = destination.with_name(f"{destination.name}.previous")
        try:
            self.status_var.set("Kicsomagolas folyamatban...")
            self.root.update_idletasks()
            source_dir = extract_payload(staging_root)

            if backup_dir.exists():
                shutil.rmtree(backup_dir, ignore_errors=True)

            if destination.exists():
                shutil.move(str(destination), str(backup_dir))

            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source_dir, destination)

            target_exe = destination / "TecsoLetolto.exe"
            if self.shortcut_var.get():
                create_desktop_shortcut(target_exe)

            if backup_dir.exists():
                shutil.rmtree(backup_dir, ignore_errors=True)

            self.status_var.set(f"Sikeres telepites: {destination}")
            messagebox.showinfo("Kesz", f"A TecsoLetolto telepitese sikerult ide:\n{destination}")

            if self.launch_var.get():
                subprocess.Popen([str(target_exe)], cwd=str(destination))
        except Exception as exc:
            if destination.exists():
                shutil.rmtree(destination, ignore_errors=True)
            if backup_dir.exists():
                shutil.move(str(backup_dir), str(destination))
            messagebox.showerror("Telepitesi hiba", f"A telepites megszakadt.\n\n{exc}")
            self.status_var.set("Telepitesi hiba tortent.")
            return
        finally:
            shutil.rmtree(staging_root, ignore_errors=True)

        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def main() -> int:
    InstallerWindow().run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
