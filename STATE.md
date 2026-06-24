# Project State

## Current status
- Stable baseline: Windows letöltés stabilizálva `.exe`-ben (yt-dlp + ffmpeg), portable/installer FFmpeg bundle támogatással.
- Branch: `otthon-2026-04-22`
- Last stable commit: `1365a32` (2026-04-22) Stabil letoltes EXE-ben; robusztusabb letoltes; ffmpeg bin bundle
- Worktree: ready for commit after completed redesign implementation.
- Completed redesign plan: `docs/codex-tasks/done/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`
- Current blocker: none. The old April runtime/build route has been removed, the fresh PyInstaller windowed GUI build was manually accepted, and the repo cleanup pass is complete.

## Last completed work
- Date: 2026-06-24
- Summary: Az aktiv ujratervezesi terv es a vendor/media dontesi fajl lezarva es `docs/codex-tasks/done/` ala mozgatva a sikeres kezi GUI smoke utan.
- Files changed: `docs/codex-tasks/done/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `docs/codex-tasks/done/vendor-and-local-media-decision-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `.venv-build\Scripts\python.exe -m pytest`; `scripts\verify_release.bat`; `git diff --check`; `scripts\clean_repo.bat`
- Result: Plan status is done; tests green (`73 passed`), release verify green, no blocker remains before commit/push.

## Last completed work
- Date: 2026-06-24
- Summary: Ovatos repo takaritas tortent a mai ujratervezes utan. Torolve lettek az ures lokalis `.agents/`, `.codex/` mappak es a lokalis `.serena/` index/cache. A friss `release/`, `artifacts/`, `vendor/` payload es az aktiv `.venv-build/` megmaradt. A `scripts/clean_repo.bat` kibovult cache/build koztesek torlesere.
- Files changed: `scripts/clean_repo.bat`, `docs/codex-tasks/repo_cleanup_report.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `git status --short --branch --ignored`; cleanup dry-runs; `scripts\clean_repo.bat`; pending final `git diff --check`
- Result: Local non-source helper/cache directories removed without touching source, release payload, vendor payload, artifacts, or build virtualenv.

## Last completed work
- Date: 2026-06-24
- Summary: A release build PyInstaller `--windowed` modra valtott, hogy inditaskor ne nyiljon kulon CMD ablak, csak a GUI. A kesz `TecsoLetolto.exe` PE subsystem erteke `2`, vagyis Windows GUI.
- Files changed: `scripts/tools/build-release.ps1`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `scripts\build_release.bat`; `.venv-build\Scripts\python.exe -c "import pefile; ..."`; `scripts\verify_release.bat`; `git diff --check`
- Result: Release build green; release self-check OK; PE subsystem `2` confirms windowed GUI executable. Manual re-check needed: launch from Explorer and confirm no CMD window appears.

## Last completed work
- Date: 2026-06-24
- Summary: Tovabb stabilizalva lett a notification-area visszanyitas. A Win32 tray callback mar nem indit kozvetlen Tk muveletet es nem bont tray hookot; csak visszanyitasi jelzot allit. A Tk main loop 200 ms-os pollinggal veszi at ezt, es onnan futtatja a `deiconify`/`lift`/tray remove agat.
- Files changed: `src/tecsoo_letolto/gui/main_window.py`, `src/tecsoo_letolto/gui/tray.py`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `.venv-build\Scripts\python.exe -m compileall -q src\tecsoo_letolto`; `.venv-build\Scripts\python.exe -m pytest`; `scripts\build_release.bat`
- Result: Tests green: `73 passed`; release build green; release self-check OK. Manual re-check needed for tray restore in the fresh build.

## Last completed work
- Date: 2026-06-24
- Summary: Javítva lett a kezi GUI smoke alatt talalt notification-area restore crash. A tray callback most explicit 64 bites Win32 pointertipusokat hasznal a `CallWindowProcW`/`SetWindowLongPtrW` hivasoknal, es tray eltavolitaskor visszaallitja az eredeti window procedure-t, hogy ne maradjon logo Python callback.
- Files changed: `src/tecsoo_letolto/gui/tray.py`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `.venv-build\Scripts\python.exe -m compileall -q src\tecsoo_letolto`; `.venv-build\Scripts\python.exe -m pytest`; `scripts\build_release.bat`
- Result: Tests green: `73 passed`; release build green; release self-check OK. Manual re-check needed for actual tray hide/restore behavior in the fresh build.

## Last completed work
- Date: 2026-06-24
- Summary: Kezi GUI smoke visszajelzes alapjan javitva lett a Sugo, Support es ertesitesi teruletre rejtes. A Sugo mar olvashato, gorgetheto offline ablakot nyit; a Support jelentés runtime Windows/yt-dlp/FFmpeg/celmappa/log adatokat tolt; az `Ertesitesi teruletre` gomb Windows tray ikont hoz letre es elrejti az ablakot.
- Files changed: `src/tecsoo_letolto/gui/main_window.py`, `src/tecsoo_letolto/gui/help_text.py`, `src/tecsoo_letolto/gui/tray.py`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `.venv-build\Scripts\python.exe -m pytest`; `.venv-build\Scripts\python.exe -m compileall -q src\tecsoo_letolto`; `scripts\build_release.bat`; `git diff --check`
- Result: Tests green: `73 passed`; release build green; release self-check OK. Manual re-check needed for actual tray restore click behavior.

## Last completed work
- Date: 2026-06-24
- Summary: Bekerult a process-szintu yt-dlp streaming es cancel flow, valamint a GUI-bol indithato, felhasznaloi jovahagyasos yt-dlp frissites. A DownloadManager progress esemenyeket kuld, CancelToken alapjan megszakit, a GUI pedig thread-safe progress frissitest es valodi cancel kerest hasznal.
- Files changed: `src/tecsoo_letolto/core/download_manager.py`, `src/tecsoo_letolto/core/progress.py`, `src/tecsoo_letolto/utils/subprocess_runner.py`, `src/tecsoo_letolto/gui/main_window.py`, `src/tecsoo_letolto/services/update_service.py`, `tests/core/test_progress.py`, `tests/core/test_download_manager.py`, `tests/services/test_update_service.py`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: targeted `.venv-build\Scripts\python.exe -m pytest tests\services\test_update_service.py tests\core\test_download_manager.py tests\core\test_progress.py tests\gui\test_view_model.py`; `.venv-build\Scripts\python.exe -m pytest`; `scripts\build_release.bat`; `git diff --check`
- Result: Targeted tests green: `24 passed`; full tests green: `73 passed`; release build green. Release self-check OK with yt-dlp `2026.06.09` and FFmpeg `N-125258-gdf94900c98-20260624`. ZIP artifact regenerated: `artifacts\TecsoLetolto-0.1.0-dev.zip`.

## Last completed work
- Date: 2026-06-24
- Summary: A release pipeline mar tenyleges PyInstaller one-folder buildet keszit `release\TecsoLetolto\` ala, bemasolja a jovahagyott vendor `yt-dlp.exe`, `ffmpeg.exe`, `ffprobe.exe` fajlokat, manifestet ir, `scripts\verify_release.bat` alatt `--version` + `--self-check` validaciot futtat, majd ZIP artifactot keszit. A regi aprilisi futtatasi/build utvonalak es regi lokalis maradekok torolve lettek.
- Files changed: `.gitignore`, `README.md`, `scripts/build_release.bat`, `scripts/verify_release.bat`, `scripts/tools/build-release.ps1`, `scripts/tools/pyinstaller-entry.py`, `docs/codex-tasks/repo_cleanup_report.md`, `docs/codex-tasks/pending/not-started/vendor-and-local-media-decision-2026-06-24.md`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`; deleted old files: `letolto.py`, `letolto_gui.py`, `run.bat`, `run_gui.bat`, `run_gui_debug.bat`, `build_exe.bat`, `build_portable_installer.bat`, `requirements.txt`, `installer/build_installer.py`, `installer/installer_app.py`
- Tests/builds run: `scripts\build_release.bat`; `scripts\verify_release.bat`; `.venv-build\Scripts\python.exe -m pytest`; release `TecsoLetolto.exe --version`; release `TecsoLetolto.exe --self-check`
- Result: Release build zold. `68 passed`; release version `0.1.0-dev`; self-check OK: app-version, logs-dir-writable, downloads-dir-writable, yt-dlp `2026.06.09`, FFmpeg `N-125258-gdf94900c98-20260624`. ZIP artifact: `artifacts\TecsoLetolto-0.1.0-dev.zip`. Regi April route removed.

## Last completed work
- Date: 2026-06-24
- Summary: Emberi jovahagyas utan torolve lett a repo alatti `downloads/` mappa, amely tesztek soran letoltott mediaanyagokat tartalmazott. A vendor/media dontesi fajl es repo cleanup riport frissult.
- Files changed: `docs/codex-tasks/pending/not-started/vendor-and-local-media-decision-2026-06-24.md`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `docs/codex-tasks/repo_cleanup_report.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: pending in current turn.
- Result: `downloads/` removed from working tree. No vendor/media decision blocker remains.

## Last completed work
- Date: 2026-06-24
- Summary: Rogzult az FFmpeg/FFprobe vendor forrasszabaly: BtbN/FFmpeg-Builds `ffmpeg-master-latest-win64-lgpl.zip`, csak `ffmpeg.exe` es `ffprobe.exe` release payload, GPL/full/nonfree fallback nelkul. Bekerult a fetch script es a vendor metaadatokat iro build manifest script.
- Files changed: `.gitignore`, `scripts/fetch_ffmpeg_vendor.bat`, `scripts/tools/fetch-ffmpeg-vendor.ps1`, `scripts/write_build_manifest.bat`, `scripts/tools/write-build-manifest.ps1`, `scripts/build_release.bat`, `docs/BUILD.md`, `docs/RELEASE.md`, `docs/THIRD_PARTY_LICENSES.md`, `docs/codex-tasks/pending/not-started/vendor-and-local-media-decision-2026-06-24.md`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `scripts\fetch_ffmpeg_vendor.bat`; `scripts\write_build_manifest.bat`; `.venv-build\Scripts\python.exe -m pytest`; `git diff --check`
- Result: FFmpeg vendor decision implemented in scripts/docs. BtbN asset found: `ffmpeg-master-latest-win64-lgpl.zip`. `ffmpeg.exe -version` and `ffprobe.exe -version` passed. Manifest includes FFmpeg/FFprobe versions, SHA-256 hashes and source URL. Tests green: `68 passed`; whitespace check clean. Local `downloads/` deletion decision remains open.

## Last completed work
- Date: 2026-06-24
- Summary: Rogzult a vendor `yt-dlp.exe` forrasszabaly: hivatalos `yt-dlp/yt-dlp` stable GitHub latest release, SHA-256 ellenorzessel, forrasrepoba commitolt binaris nelkul. Bekerult a `scripts\fetch_ytdlp_vendor.bat` es a PowerShell letolto/ellenorzo script, valamint az updater service SHA-256 helper alapja.
- Files changed: `.gitignore`, `scripts/fetch_ytdlp_vendor.bat`, `scripts/tools/fetch-ytdlp-vendor.ps1`, `scripts/build_release.bat`, `src/tecsoo_letolto/services/update_service.py`, `tests/services/test_update_service.py`, `docs/BUILD.md`, `docs/RELEASE.md`, `docs/THIRD_PARTY_LICENSES.md`, `docs/codex-tasks/pending/not-started/vendor-and-local-media-decision-2026-06-24.md`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `scripts\fetch_ytdlp_vendor.bat`; `.venv-build\Scripts\python.exe -m pytest`; `git diff --check`
- Result: yt-dlp vendor decision implemented in scripts/docs. Official stable `yt-dlp.exe` downloaded from GitHub, version `2026.06.09`, SHA-256 verified: `3a48cb955d55c8821b60ccbdbbc6f61bc958f2f3d3b7ad5eaf3d83a543293a27`. Tests green: `68 passed`; whitespace check clean. FFmpeg vendor/licenc and local `downloads/` deletion decisions remain open.

## Last completed work
- Date: 2026-06-24
- Summary: Pontositva lett az aktiv terv `pyproject.toml` fuggesegi szabalyzata: runtime dependencies minimalis/ures, `pytest` csak `test` extra, `pyinstaller` csak `build` extra.
- Files changed: `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `.venv-build\Scripts\python.exe -m pytest`; `git diff --check`
- Result: Tervszoveg tisztazva, a tenyleges `pyproject.toml` mar eleve megfelelt ennek a szetvalasztasnak.

## Last completed work
- Date: 2026-06-24
- Summary: Celzott audit utan rogzult a kovetkezo emberi dontespont: vendor komponensek forrasa/licence, es a helyi `downloads/` media mappa torolhetosege.
- Files changed: `docs/codex-tasks/pending/not-started/vendor-and-local-media-decision-2026-06-24.md`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `.venv-build\Scripts\python.exe -m pytest`; `git diff --check`; targeted `rg` secret/path scan
- Result: Tesztek zoldok (`65 passed`) es whitespace check tiszta. A scan csak synthetic teszt/dokumentacios talalatokat es ismert regi futtatasi utvonalakban levo `E:\ffmpeg...` maradekokat jelzett. A regi utvonalak torlese az uj release validacioja utan biztonsagos.

## Last completed work
- Date: 2026-06-24
- Summary: Bekerult a dokumentacios es script skeleton: felhasznaloi README irany, user/support/build/release docs, release checklist, third-party license vaz, fejlesztoi build wrapper, release verify vaz es cleanup riport.
- Files changed: `README.md`, `docs/CHANGELOG.md`, `docs/USER_GUIDE.md`, `docs/SUPPORT.md`, `docs/BUILD.md`, `docs/RELEASE.md`, `docs/RELEASE_TEST_CHECKLIST.md`, `docs/THIRD_PARTY_LICENSES.md`, `docs/codex-tasks/repo_cleanup_report.md`, `scripts/build_dev.bat`, `scripts/build_release.bat`, `scripts/verify_release.bat`, `scripts/clean_repo.bat`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `scripts\build_dev.bat`; `.venv-build\Scripts\python.exe -m pytest`; `git diff --check`
- Result: Fejlesztoi build wrapper zold, tesztek zoldok (`65 passed`). A release build meg vendor/preflight vaz, nem kesz csomag.

## Last completed work
- Date: 2026-06-24
- Summary: Bekerult a kezi yt-dlp frissites service alap. A service csak `yt-dlp.exe` cseret enged, ellenorzi az uj fajl futtathatosagat, backupot keszit `yt-dlp.previous.exe` nevvel, es rollbacket tud.
- Files changed: `src/tecsoo_letolto/services/update_service.py`, `tests/services/test_update_service.py`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `.venv-build\Scripts\python.exe -m pytest`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`; `git diff --check`
- Result: Tesztek zoldok (`65 passed`), version smoke OK, whitespace check tiszta. A GUI frissites gomb es a felhasznaloi jovahagyasi dialog meg nyitott.

## Last completed work
- Date: 2026-06-24
- Summary: A GUI `Letöltés indítása` gombja worker threaden keresztul bekotodott a `DownloadManager` backendhez. Hiba eseten a domain hibak magyar, felhasznaloi uzenette alakulnak.
- Files changed: `src/tecsoo_letolto/gui/main_window.py`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `.venv-build\Scripts\python.exe -m pytest`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`; `git diff --check`
- Result: Tesztek zoldok (`59 passed`), version smoke OK, whitespace check tiszta. A process-szintu cancel/progress streaming meg nyitott; a cancel gomb jelenleg csak jelzi, hogy ez a kovetkezo backend szelet.

## Last completed work
- Date: 2026-06-24
- Summary: Bekerult a szinkron `DownloadManager` backend alap. A manager mar biztonsagos output pathot valaszt, ellenorzi az irhato mentési mappat, megkeresi a vendor FFmpeg/yt-dlp eszkozoket, megépiti a yt-dlp parancsot, es hiba eseten domain hibara mappel.
- Files changed: `src/tecsoo_letolto/core/download_manager.py`, `tests/core/test_download_manager.py`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `.venv-build\Scripts\python.exe -m pytest`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`; `git diff --check`
- Result: Tesztek zoldok (`59 passed`), version smoke OK, whitespace check tiszta. A GUI worker bekotes es progress/cancel streaming meg nyitott.

## Last completed work
- Date: 2026-06-24
- Summary: Bekerult a GUI view-model es az egyablakos Tk main window scaffold. A felulet csak a tervben engedelyezett mezoket es gombokat tartalmazza, nem kerult bele playlist, cookie, login, proxy vagy halado yt-dlp opcio.
- Files changed: `src/tecsoo_letolto/app.py`, `src/tecsoo_letolto/gui/main_window.py`, `src/tecsoo_letolto/gui/view_model.py`, `tests/gui/__init__.py`, `tests/gui/test_view_model.py`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `.venv-build\Scripts\python.exe -m pytest`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`; `git diff --check`
- Result: Tesztek zoldok (`55 passed`), version smoke OK, whitespace check tiszta. A GUI automata megnyitasa nem tortent; a tenyleges download backend bekotese meg nyitott.

## Last completed work
- Date: 2026-06-24
- Summary: Bekerult a support report alap, a napi UTF-8 log konfiguracio es a self-check parancs. A support report roviditi az URL-t, redaktalja a secret jellegu adatokat, es `mailto:` linket keszit SMTP nelkul.
- Files changed: `src/tecsoo_letolto/app.py`, `src/tecsoo_letolto/core/self_check.py`, `src/tecsoo_letolto/core/support_report.py`, `src/tecsoo_letolto/utils/logging_setup.py`, `tests/core/test_self_check.py`, `tests/core/test_support_report.py`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `STATE.md`, `docs/CHANGELOG.dev.md`
- Tests/builds run: `.venv-build\Scripts\python.exe -m pytest`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --self-check`; `git diff --check`
- Result: Tesztek zoldok (`49 passed`), version smoke OK. A valos self-check mukodik, de a jelenlegi dev repoban vendor `yt-dlp.exe` es FFmpeg hianya miatt `FAIL yt-dlp` es `FAIL ffmpeg` eredmenyt ad; ez a build/vendor szelet nyitott feladata.

## Last completed work
- Date: 2026-06-24
- Summary: A masodik P&P implementacios szeletben bekerult a kategorizalt hibatérkép, support-adat redakcio, biztonsagos subprocess runner, FFmpeg/ffprobe service alap, yt-dlp service alap es audio/video argumentumepites.
- Files changed: `src/tecsoo_letolto/core/error_mapping.py`, `src/tecsoo_letolto/core/media_info.py`, `src/tecsoo_letolto/core/progress.py`, `src/tecsoo_letolto/services/ffmpeg_service.py`, `src/tecsoo_letolto/services/ytdlp_service.py`, `src/tecsoo_letolto/utils/redaction.py`, `src/tecsoo_letolto/utils/subprocess_runner.py`, `tests/core/test_error_mapping.py`, `tests/services/test_ffmpeg_service.py`, `tests/services/test_ytdlp_service.py`, `tests/utils/test_redaction.py`, `tests/utils/test_subprocess_runner.py`
- Tests/builds run: `.venv-build\Scripts\python.exe -m pytest`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`; `git diff --check`
- Result: Teljes eddigi tesztkeszlet zold (`42 passed`), version smoke OK (`0.1.0-dev`), whitespace check tiszta.

## Last completed work
- Date: 2026-06-24
- Summary: Elindult a P&P ujratervezesi terv vegrehajtasa. Letrejott a Python package scaffold, `pyproject.toml`, az elso core hibamodellek, a Windows-biztos fajlnev policy es az alap path/log/output directory policy.
- Files changed: `pyproject.toml`, `.gitignore`, `src/tecsoo_letolto/**`, `tests/core/test_filename_policy.py`, `tests/core/test_paths.py`, `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `docs/CHANGELOG.dev.md`, `STATE.md`
- Tests/builds run: `py -3.12 -m venv .venv-build`; `.venv-build\Scripts\python.exe -m pip install -e .[test]`; `.venv-build\Scripts\python.exe -m pytest tests\core`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`
- Result: `tests\core` zold (`19 passed`), package version smoke OK (`0.1.0-dev`). A regi `letolto.py` / `letolto_gui.py` futtatasi utvonal meg erintetlen.

## Last completed work
- Date: 2026-06-24
- Summary: `docs/ujratervezés.md` alapjan elkeszult a reszletes, email-header-analyzer mintaju P&P ujratervezesi terv. A terv a jelenlegi monolit `letolto.py` / `letolto_gui.py` szerkezetet celzott `src/tecsoo_letolto/` modulokra bontja, es kulon rogzit build, release, teszt, support, licence, fajlkovetes es repo-takaritas kapukat.
- Files changed: `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`, `docs/CHANGELOG.dev.md`, `STATE.md`
- Tests/builds run: dokumentacios audit es forrasolvasas; automatizalt teszt/build nem futott, mert implementacio nem tortent.
- Result: A kovetkezo fejlesztesi lepes mar konkretan indithato: `pyproject.toml`, `core/filename_policy.py`, `core/paths.py`, es ezek unit tesztjei.

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
