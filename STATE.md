# Project State

## Current status
- Stable baseline: Windows letöltés stabilizálva `.exe`-ben (yt-dlp + ffmpeg), portable/installer FFmpeg bundle támogatással.
- Branch: `otthon-2026-04-22`
- Last stable commit: `1365a32` (2026-04-22) Stabil letoltes EXE-ben; robusztusabb letoltes; ffmpeg bin bundle
- Worktree: has local doc changes (`AGENTS.md`, `STATE.md`) pending commit

## Last completed work
- Date: 2026-04-22 (feature fix), 2026-04-24 (state tracking docs)
- Summary: 416/resume fallback + file-lock/resume stabilizálás; FFmpeg `bin` bundle; most `STATE.md` bevezetés a folytathatósághoz.
- Files changed: `letolto.py`, `letolto_gui.py`, `installer/build_installer.py`, `README.md`, `AGENTS.md`, `STATE.md`
- Tests/builds run: (not recorded here yet)
- Result: Letöltés stabilabb Windows-on; következő lépés előtt érdemes egy end-to-end próbát rögzíteni.

## Known issues
- End-to-end (GUI) validáció eredménye nincs még rögzítve ebben a fájlban.

## Next steps
- 1. Döntés: merge/release a `master` felé, vagy előbb end-to-end ellenőrzés (GUI letöltés + 416 fallback).
- 2. Ha end-to-end ok: rögzítsd itt a konkrét parancsot/lépést + eredményt.
- 3. Commit + push `AGENTS.md` + `STATE.md`.

## Important decisions
- Decision: 416 esetén `.part` takarítás + retry resume nélkül (`continuedl=False`).
- Reason: A HTTP 416 tipikusan stale partial/resume állapotból jön; a “clean retry” a legkisebb stabil javítás.

## Do not forget
- Portable buildnél az FFmpeg bundle része; ne hivatkozz abszolút gépspecifikus FFmpeg path-ra a `STATE.md`-ben.
