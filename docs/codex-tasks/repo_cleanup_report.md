# Repo cleanup report

## Status

- Allapot: reszleges vegleges takaritas megtortent.
- Ok: az uj PyInstaller one-folder release self-check zold lett, ezert a regi aprilisi futtatasi es build utvonalak eltavolithatok voltak.

## Torolt vagy kivaltott

- `letolto.py`
  - Ok: regi monolit CLI/backend.
  - Allapot: torolve 2026-06-24-en, miutan `release\TecsoLetolto\TecsoLetolto.exe --self-check` zold lett.
- `letolto_gui.py`
  - Ok: regi monolit Tk GUI.
  - Allapot: torolve 2026-06-24-en, az uj `src/tecsoo_letolto/gui/main_window.py` es PyInstaller entrypoint valtja ki.
- `run.bat`, `run_gui.bat`, `run_gui_debug.bat`
  - Ok: regi inditasi utvonalak.
  - Allapot: torolve 2026-06-24-en; `TecsoLetolto.exe`, `--version`, `--self-check` es `scripts\build_release.bat` valtja ki.
- `build_exe.bat`, `build_portable_installer.bat`
  - Ok: regi build utvonal.
  - Allapot: torolve 2026-06-24-en; `scripts/build_release.bat` es `scripts/verify_release.bat` valtja ki.
- `installer/`
  - Ok: regi installer megoldas.
  - Allapot: torolve 2026-06-24-en; az elso release cel PyInstaller one-folder portable mappa.
- `requirements.txt`
  - Ok: regi pip-alapu `yt-dlp` dependency, ellentetes az uj vendor dontessel.
  - Allapot: torolve 2026-06-24-en; `pyproject.toml` optional `test` es `build` extrak valtjak ki.
- `downloads/`
  - Ok: user media, nem repo payload.
  - Allapot: torolve 2026-06-24-en emberi jovahagyas utan.
  - Megjegyzes: a mappa teszt soran letoltott mediafajlokat tartalmazott, nem forras- vagy release-payload volt.
- `artifacts/TecsoLetolto.exe`, `artifacts/TecsoLetolto-Installer.exe`
  - Ok: regi/lokalis build artifactok, nem forraskod.
  - Allapot: torolve 2026-06-24-en; az aktualis artifact `artifacts/TecsoLetolto-0.1.0-dev.zip` es `artifacts/build_manifest.json`.
- `.agents/`, `.codex/`
  - Ok: ures lokalis segedmappak, nem projektforras.
  - Allapot: torolve 2026-06-24-en.
- `.serena/`
  - Ok: lokalis Serena index/cache, nem projektforras.
  - Allapot: torolve 2026-06-24-en. Ha Serena kesobb ujrageneralja, `scripts/clean_repo.bat` ujra torolheti.

## Kesobb torlendo vagy kivaltando

- `artifacts/`
  - Ok: build output, nem forraskod.
  - Feltetel: torles elott ellenorizni kell, hogy nincs szukseges release artifact. Jelenleg a friss ZIP es manifest megtartva.
- `release/`
  - Ok: build output, nem forraskod.
  - Feltetel: release artifact keszites utan ujrageneralhato.
- `__pycache__/`, `*.pyc`
  - Ok: Python cache.
  - Feltetel: barmikor torolheto `scripts/clean_repo.bat` segitsegevel.
- `.pytest_cache/`, `*.egg-info`, `build/`, `dist/`, `TecsoLetolto.spec`, `.serena/`
  - Ok: lokalis teszt/build/tool cache vagy koztes output.
  - Feltetel: barmikor torolheto `scripts/clean_repo.bat` segitsegevel.
- `.venv/`, `.venv-build/`
  - Ok: lokalis virtualenv.
  - Feltetel: nem Git payload, torles csak ha nincs aktiv fejlesztesi futas.

## Megtartando

- `assets/tecsoo-letolto.ico`
  - Ok: ikon asset, kesobb atemelheto `src/tecsoo_letolto/resources/app.ico` ala.
- `docs/ujratervezés.md`
  - Ok: forras tervanyag.
- `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`
  - Ok: aktiv megvalositasi terv.
- `STATE.md`
  - Ok: repo allapotmemoria.
- `AGENTS.md`
  - Ok: repo-local agent szabaly.

## Ismert kockazatok

- A regi `letolto.py` es README korabban gepfuggo FFmpeg peldat tartalmazott; az uj runtime kodban ilyen fallback nem maradhat.
- A `downloads/` mappa torlese csak emberi jovahagyassal tortenhet; a 2026-06-24-i helyi tesztmedia torles jovahagyva es elvegezve.
- A release vendor komponensek forrasa rogzitett: yt-dlp official stable GitHub release, FFmpeg BtbN LGPL win64 static zip.
