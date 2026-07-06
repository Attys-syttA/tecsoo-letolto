# TecsoLetolto fejlesztoi changelog

Append-only fejlesztoi naplo. A felhasznaloi release valtozasok kulon `docs/CHANGELOG.md` ala keruljenek, amikor a release folyamat elindul.

## 2026-07-06 13:22 +02:00

- Cel: Friss, a mostani GUI payloadbol epulo Windows installer build visszaallitasa a regi aprilisi telepito lecserelesere.
- Modositott fajlok: `scripts/build_installer.bat`; `scripts/tools/build-installer.ps1`; `scripts/tools/installer-bootstrap.py`; `scripts/tools/package-release.py`; `scripts/tools/build-release.ps1`; `README.md`; `docs/BUILD.md`; `docs/RELEASE.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `scripts\build_installer.bat`; `Get-Item artifacts\TecsoLetolto-Installer.exe`; `Get-FileHash artifacts\TecsoLetolto-Installer.exe -Algorithm SHA256`; kezi artifact masolat: `TecsoLetolto-Installer-0.1.0-dev.exe`.
- Eredmeny: Sikeresen legyartva a friss telepito a jelenlegi release payloadbol. Az installer mar nem a regi IExpress csomag, hanem PyInstaller-alapu GUI telepito. A release ZIP csomagolas retry vedelmet kapott a rovid ideju ffmpeg fajlzarat ellen.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: kezi telepitesi smoke a friss `TecsoLetolto-Installer-0.1.0-dev.exe` futtatassal.

## 2026-06-24 17:45 +02:00

- Cel: `docs/ujratervezés.md` alapjan reszletes, email-header-analyzer mintaju P&P ujratervezesi terv keszitese.
- Modositott fajlok: `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `docs/CHANGELOG.dev.md`; `STATE.md`.
- Futtatott parancsok: `git status --short --branch`; `Get-Content STATE.md`; `Get-Content docs\ujratervezés.md`; `rg --files` es relevans docs mintak olvasasa az `email-header-analyzer` repoban; jelenlegi `letolto.py`, `letolto_gui.py`, installer scriptek, README es `.gitignore` atnezese.
- Eredmeny: Letrejott az aktiv megvalositasi terv a `docs/codex-tasks/pending/active/` mappaban, statuszblokkal, modulokra bontott implementacios tervvel, teszt- es release-kapukkal.
- Verzio: nincs bump, mert csak dokumentacios/tervezesi valtozas tortent.
- Nyitott follow-up: elso implementacios szelet: `pyproject.toml`, `core/filename_policy.py`, `core/paths.py`, es ezek unit tesztjei.

## 2026-06-24 18:18 +02:00

- Cel: A P&P ujratervezesi terv elso implementacios szelete: package scaffold, fajlnev policy, path policy es unit tesztek.
- Modositott fajlok: `pyproject.toml`; `.gitignore`; `src/tecsoo_letolto/__init__.py`; `src/tecsoo_letolto/__main__.py`; `src/tecsoo_letolto/app.py`; `src/tecsoo_letolto/version.py`; `src/tecsoo_letolto/core/__init__.py`; `src/tecsoo_letolto/core/errors.py`; `src/tecsoo_letolto/core/filename_policy.py`; `src/tecsoo_letolto/core/paths.py`; `src/tecsoo_letolto/gui/__init__.py`; `src/tecsoo_letolto/services/__init__.py`; `src/tecsoo_letolto/utils/__init__.py`; `tests/core/__init__.py`; `tests/core/test_filename_policy.py`; `tests/core/test_paths.py`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `py -3.12 -m pytest tests\core` (pytest hianyzott); `.venv\Scripts\python.exe -m pytest tests\core` (pytest hianyzott, es a venv Python 3.14); `py -3.12 -m venv .venv-build`; `.venv-build\Scripts\python.exe -m pip install --upgrade pip`; `.venv-build\Scripts\python.exe -m pip install -e .[test]`; `.venv-build\Scripts\python.exe -m pytest tests\core`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`.
- Eredmeny: Letrejott az uj `src/tecsoo_letolto` package alap, a `filename_policy` es `paths` core modul, valamint 19 unit teszt. A tesztek zoldok: `19 passed`. A minimal package smoke `0.1.0-dev` verziot ad vissza.
- Verzio: marad `0.1.0-dev`; ez scaffold/core alapozas, meg nincs user-facing release.
- Nyitott follow-up: `core/error_mapping.py`, `utils/subprocess_runner.py`, `services/ffmpeg_service.py`, `services/ytdlp_service.py` es tesztjeik.

## 2026-06-24 18:21 +02:00

- Cel: Hibatérkép, redakcio, subprocess runner es runtime tool service alapok bevezetese.
- Modositott fajlok: `src/tecsoo_letolto/core/error_mapping.py`; `src/tecsoo_letolto/core/media_info.py`; `src/tecsoo_letolto/core/progress.py`; `src/tecsoo_letolto/services/ffmpeg_service.py`; `src/tecsoo_letolto/services/ytdlp_service.py`; `src/tecsoo_letolto/utils/redaction.py`; `src/tecsoo_letolto/utils/subprocess_runner.py`; `tests/core/test_error_mapping.py`; `tests/services/__init__.py`; `tests/services/test_ffmpeg_service.py`; `tests/services/test_ytdlp_service.py`; `tests/utils/__init__.py`; `tests/utils/test_redaction.py`; `tests/utils/test_subprocess_runner.py`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `.venv-build\Scripts\python.exe -m pytest`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`; `git diff --check`.
- Eredmeny: A teljes eddigi tesztkeszlet zold: `42 passed`. A minimal package smoke `0.1.0-dev` verziot ad vissza. A whitespace check tiszta.
- Verzio: marad `0.1.0-dev`; meg mindig fejlesztoi scaffold es belso modulalapozas, nincs release.
- Nyitott follow-up: support report, logging, self-check, update service, GUI es release pipeline.

## 2026-06-24 18:24 +02:00

- Cel: Support report, logging setup es self-check alap bevezetese.
- Modositott fajlok: `src/tecsoo_letolto/app.py`; `src/tecsoo_letolto/core/self_check.py`; `src/tecsoo_letolto/core/support_report.py`; `src/tecsoo_letolto/utils/logging_setup.py`; `tests/core/test_self_check.py`; `tests/core/test_support_report.py`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `.venv-build\Scripts\python.exe -m pytest`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --self-check`; `git diff --check`.
- Eredmeny: Tesztek zoldok: `49 passed`. Version smoke OK. A valos self-check jelzi a vart vendor hianyt: `FAIL yt-dlp` es `FAIL ffmpeg`, mert a release vendor mappa meg nincs feltoltve.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: GUI view-model, GUI ablak, update service es build/vendor pipeline.

## 2026-06-24 18:26 +02:00

- Cel: GUI view-model es egyablakos Tk scaffold bevezetese a scope-korlatozott P&P felulethez.
- Modositott fajlok: `src/tecsoo_letolto/app.py`; `src/tecsoo_letolto/gui/main_window.py`; `src/tecsoo_letolto/gui/view_model.py`; `tests/gui/__init__.py`; `tests/gui/test_view_model.py`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `.venv-build\Scripts\python.exe -m pytest`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`; `git diff --check`.
- Eredmeny: Tesztek zoldok: `55 passed`. Az app normal modban mar a GUI belépési pontot inditja, mikozben a `--version` es `--self-check` CLI parancs megmaradt.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: download manager backend bekotese es GUI download worker.

## 2026-06-24 18:27 +02:00

- Cel: Szinkron download manager backend alap bevezetese.
- Modositott fajlok: `src/tecsoo_letolto/core/download_manager.py`; `tests/core/test_download_manager.py`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `.venv-build\Scripts\python.exe -m pytest`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`; `git diff --check`.
- Eredmeny: Tesztek zoldok: `59 passed`. A backend mar valaszt output pathot, ellenorzi a vendor toolokat, epiti es futtatja a yt-dlp parancsot, majd hibat domain hibara mappel.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: GUI worker bekotes, progress/cancel streaming, build/vendor pipeline.

## 2026-06-24 18:29 +02:00

- Cel: GUI `Letöltés indítása` gomb bekotese a `DownloadManager` backendhez worker threaden.
- Modositott fajlok: `src/tecsoo_letolto/gui/main_window.py`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `.venv-build\Scripts\python.exe -m pytest`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`; `git diff --check`.
- Eredmeny: Tesztek zoldok: `59 passed`. A GUI start gomb mar nem placeholder, hanem backend worker threadet indit; hiba eseten magyar user-facing hibaablakot kap a felhasznalo.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: process-szintu cancel/progress streaming, vendor/build pipeline.

## 2026-06-24 18:30 +02:00

- Cel: Kezi yt-dlp frissites service alap bevezetese rollback vedelmi reteggel.
- Modositott fajlok: `src/tecsoo_letolto/services/update_service.py`; `tests/services/test_update_service.py`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `.venv-build\Scripts\python.exe -m pytest`; `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`; `git diff --check`.
- Eredmeny: Tesztek zoldok: `65 passed`. Az updater service csak `yt-dlp.exe` targetet cserelhet, backupot keszit es rollbacket tud.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: GUI frissites gomb/jovahagyasi dialog, build/vendor pipeline.

## 2026-06-24 18:33 +02:00

- Cel: Dokumentacios es build/release script skeleton bevezetese.
- Modositott fajlok: `README.md`; `docs/CHANGELOG.md`; `docs/USER_GUIDE.md`; `docs/SUPPORT.md`; `docs/BUILD.md`; `docs/RELEASE.md`; `docs/RELEASE_TEST_CHECKLIST.md`; `docs/THIRD_PARTY_LICENSES.md`; `docs/codex-tasks/repo_cleanup_report.md`; `scripts/build_dev.bat`; `scripts/build_release.bat`; `scripts/verify_release.bat`; `scripts/clean_repo.bat`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `scripts\build_dev.bat`; `.venv-build\Scripts\python.exe -m pytest`; `git diff --check`.
- Eredmeny: A fejlesztoi build wrapper zold, a tesztek tovabbra is zoldok: `65 passed`. A release script jelenleg vendor preflight vaz, a teljes csomagolas meg nyitott.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: PyInstaller packaging, vendor input/fetch dontes, build manifest, GUI update dialog, progress/cancel streaming.

## 2026-06-24 18:35 +02:00

- Cel: Blokkolo emberi dontespontok rogzítese a teljes P&P terv folytatasa elott.
- Modositott fajlok: `docs/codex-tasks/pending/not-started/vendor-and-local-media-decision-2026-06-24.md`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `.venv-build\Scripts\python.exe -m pytest`; `git diff --check`; `rg -n "password|passwd|secret|token|apikey|api_key|smtp|FFMPEG_DIR|E:\\|C:\\Users|192\\.168\\.|172\\.16\\." ...`.
- Eredmeny: Tesztek zoldok: `65 passed`; whitespace check tiszta. A celzott scan ismert regi futtatasi utvonalakban jelzett `E:\ffmpeg...` maradekot, tovabba synthetic teszt/dokumentacios talalatokat.
- Verzio: marad `0.1.0-dev`.
- Blokkolo follow-up: emberi dontes kell a vendor FFmpeg/yt-dlp forrasrol/licencrol, es a helyi `downloads/` media torolhetosegerol.

## 2026-06-24 18:36 +02:00

- Cel: `pyproject.toml` fuggesegi szerepek tisztazasa az aktiv tervben.
- Modositott fajlok: `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `.venv-build\Scripts\python.exe -m pytest`; `git diff --check`.
- Eredmeny: A terv mar kulon kezeli a runtime dependencies, dev/test dependencies es build dependencies szerepeket. A tenyleges `pyproject.toml` mar eddig is `dependencies = []`, `test = pytest`, `build = pyinstaller` szerkezetu volt.
- Verzio: nincs bump, mert dokumentacios/terv pontositas.
- Nyitott follow-up: vendor/licenc dontes es teljes release packaging.

## 2026-06-24 18:40 +02:00

- Cel: A vendor `yt-dlp.exe` forrasara hozott emberi dontes atvezetese a build scriptbe, updater helperbe es dokumentacioba.
- Modositott fajlok: `.gitignore`; `scripts/fetch_ytdlp_vendor.bat`; `scripts/tools/fetch-ytdlp-vendor.ps1`; `scripts/build_release.bat`; `src/tecsoo_letolto/services/update_service.py`; `tests/services/test_update_service.py`; `docs/BUILD.md`; `docs/RELEASE.md`; `docs/THIRD_PARTY_LICENSES.md`; `docs/codex-tasks/pending/not-started/vendor-and-local-media-decision-2026-06-24.md`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `scripts\fetch_ytdlp_vendor.bat`; `.venv-build\Scripts\python.exe -m pytest`; `git diff --check`.
- Eredmeny: A build elokeszites a hivatalos `yt-dlp/yt-dlp` stable GitHub release `yt-dlp.exe` fajljat tolti le, `SHA2-256SUMS` alapjan ellenorzi, majd `vendor/yt-dlp/` ala teszi. Ellenorzott verzio: `2026.06.09`; SHA-256: `3a48cb955d55c8821b60ccbdbbc6f61bc958f2f3d3b7ad5eaf3d83a543293a27`. A `vendor/` mappa gitignored, a binaris csak release payload lehet. Tesztek zoldok: `68 passed`; whitespace check tiszta.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: FFmpeg vendor forras/licenc dontes, build manifest teljes generalasa, PyInstaller packaging, helyi `downloads/` torolhetosege.

## 2026-06-24 18:50 +02:00

- Cel: Az FFmpeg/FFprobe vendor forrasara hozott emberi dontes atvezetese a build scriptbe, manifestbe es dokumentacioba.
- Modositott fajlok: `.gitignore`; `scripts/fetch_ffmpeg_vendor.bat`; `scripts/tools/fetch-ffmpeg-vendor.ps1`; `scripts/write_build_manifest.bat`; `scripts/tools/write-build-manifest.ps1`; `scripts/build_release.bat`; `docs/BUILD.md`; `docs/RELEASE.md`; `docs/THIRD_PARTY_LICENSES.md`; `docs/codex-tasks/pending/not-started/vendor-and-local-media-decision-2026-06-24.md`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `scripts\fetch_ffmpeg_vendor.bat`; `scripts\write_build_manifest.bat`; `.venv-build\Scripts\python.exe -m pytest`; `git diff --check`.
- Eredmeny: A build elokeszites csak a BtbN/FFmpeg-Builds `ffmpeg-master-latest-win64-lgpl.zip` assetet fogadja el. A script csak `ffmpeg.exe` es `ffprobe.exe` fajlt masol a vendor runtime bin mappaba; GPL/full/nonfree fallback nincs automatikusan. Ellenorzott FFmpeg verzio: `N-125258-gdf94900c98-20260624`; `ffmpeg.exe` SHA-256: `6967a5a15f51689c32731a69fd25ce8ff06dd940a6e46fc7925d73b09faa8e24`; `ffprobe.exe` SHA-256: `2aaeebfc083936f83f00c1a51b6196b05c61baef5f9516cd57c36254893ef293`. Tesztek zoldok: `68 passed`; whitespace check tiszta.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: PyInstaller packaging, release ZIP artifact.

## 2026-06-24 19:05 +02:00

- Cel: A repo alatti `downloads/` tesztmedia torlesi dontes atvezetese es a mappa torlese.
- Modositott fajlok: `docs/codex-tasks/pending/not-started/vendor-and-local-media-decision-2026-06-24.md`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `docs/codex-tasks/repo_cleanup_report.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `Resolve-Path -LiteralPath downloads`; `Remove-Item -LiteralPath <repo>\downloads -Recurse -Force`.
- Eredmeny: A `downloads/` mappa torolve lett emberi jovahagyas alapjan. A mappa teszt soran letoltott mediafajlokat tartalmazott, nem forras- vagy release-payload volt.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: PyInstaller packaging, release ZIP artifact, process-szintu cancel/progress streaming, GUI update dialog.

## 2026-06-24 19:25 +02:00

- Cel: A release build pipeline tenyleges PyInstaller one-folder buildde es ZIP artifact keszitove alakitasa, majd a regi aprilisi futtatasi es build utvonalak eltavolitasa.
- Modositott fajlok: `.gitignore`; `README.md`; `scripts/build_release.bat`; `scripts/verify_release.bat`; `scripts/tools/build-release.ps1`; `scripts/tools/pyinstaller-entry.py`; `docs/codex-tasks/repo_cleanup_report.md`; `docs/codex-tasks/pending/not-started/vendor-and-local-media-decision-2026-06-24.md`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Torolt regi fajlok: `letolto.py`; `letolto_gui.py`; `run.bat`; `run_gui.bat`; `run_gui_debug.bat`; `build_exe.bat`; `build_portable_installer.bat`; `requirements.txt`; `installer/build_installer.py`; `installer/installer_app.py`.
- Torolt lokalis maradekok: regi `.venv`; `installer/`; regi artifact binarisok `artifacts/TecsoLetolto.exe` es `artifacts/TecsoLetolto-Installer.exe`; PyInstaller koztes `build/`, `dist/`, `TecsoLetolto.spec`; Python cache mappak.
- Futtatott parancsok: `scripts\build_release.bat`; `scripts\verify_release.bat`.
- Eredmeny: A release mappa letrejott `release\TecsoLetolto\` alatt. `TecsoLetolto.exe --version` OK (`0.1.0-dev`). `TecsoLetolto.exe --self-check` OK: app version, logs dir, Downloads dir, yt-dlp `2026.06.09`, FFmpeg `N-125258-gdf94900c98-20260624`. ZIP artifact: `artifacts\TecsoLetolto-0.1.0-dev.zip`. A regi April route torolve.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: process-szintu cancel/progress streaming, GUI update dialog, kezi GUI smoke checklist.

## 2026-06-24 19:35 +02:00

- Cel: Process-szintu download streaming/cancel es GUI yt-dlp update dialog bekotese.
- Modositott fajlok: `src/tecsoo_letolto/core/download_manager.py`; `src/tecsoo_letolto/core/progress.py`; `src/tecsoo_letolto/utils/subprocess_runner.py`; `src/tecsoo_letolto/gui/main_window.py`; `src/tecsoo_letolto/services/update_service.py`; `tests/core/test_progress.py`; `tests/core/test_download_manager.py`; `tests/services/test_update_service.py`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `.venv-build\Scripts\python.exe -m pytest tests\services\test_update_service.py tests\core\test_download_manager.py tests\core\test_progress.py tests\gui\test_view_model.py`; `.venv-build\Scripts\python.exe -m pytest`; `scripts\build_release.bat`; `git diff --check`.
- Eredmeny: A letoltes mar streaming runnerrel fut, progress sort parse-ol, es `CancelToken` alapjan megszakithato. A GUI cancel gomb tenyleges cancel kerest ad. A GUI yt-dlp frissites gomb verziot ellenoriz, felhasznaloi jovahagyast ker, majd csak `vendor/yt-dlp/yt-dlp.exe` fajlt cserel SHA-256 ellenorzessel. Célzott tesztek zoldok: `24 passed`; teljes teszt: `73 passed`; release build es self-check zold. ZIP artifact ujrageneralva: `artifacts\TecsoLetolto-0.1.0-dev.zip`.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: teljes validacio ebben a korben, majd kezi GUI smoke checklist.

## 2026-06-24 20:58 +02:00

- Cel: Kezi GUI smoke visszajelzes javitasa: valodi Sugo tartalom, teljesebb Support jelentés, es Windows ertesitesi teruletre rejtes.
- Modositott fajlok: `src/tecsoo_letolto/gui/main_window.py`; `src/tecsoo_letolto/gui/help_text.py`; `src/tecsoo_letolto/gui/tray.py`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `.venv-build\Scripts\python.exe -m pytest tests\core\test_support_report.py tests\gui\test_view_model.py`; `.venv-build\Scripts\python.exe -m compileall -q src\tecsoo_letolto`; `.venv-build\Scripts\python.exe -m pytest`; `scripts\build_release.bat`; `git diff --check`.
- Eredmeny: A Sugo mar beagyazott, gorgetheto magyar offline szoveget mutat. A Support report runtime Windows/yt-dlp/FFmpeg/celmappa/log adatokat probal kitolteni. Az `Ertesitesi teruletre` gomb Windows tray ikont hoz letre es az ablakot elrejti; kattintasra visszaallitasi handler van. Tesztek zoldok: `73 passed`; release build es self-check zold.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: kezi GUI smoke ujraellenorzes a tray ikon visszaallitassal.

## 2026-06-24 21:12 +02:00

- Cel: Notification-area restore crash javitasa a kezi GUI smoke alatt latott `ctypes.ArgumentError: argument 1: OverflowError: int too long to convert` hiba alapjan.
- Modositott fajlok: `src/tecsoo_letolto/gui/tray.py`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `.venv-build\Scripts\python.exe -m compileall -q src\tecsoo_letolto`; `.venv-build\Scripts\python.exe -m pytest`; `scripts\build_release.bat`.
- Eredmeny: A tray window procedure callback explicit 64 bites pointertipusokat kapott a `CallWindowProcW`/`SetWindowLongPtrW` hivasokhoz, es tray eltavolitaskor visszaallitja az eredeti wndproc-ot. Teljes teszt: `73 passed`; release build es self-check zold. ZIP artifact ujrageneralva: `artifacts\TecsoLetolto-0.1.0-dev.zip`.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: kezi GUI smoke ujraellenorzes a friss builddel, kulonosen az ertesitesi teruletre rejtes es visszanyitas.

## 2026-06-24 21:21 +02:00

- Cel: Notification-area visszanyitas tovabbi stabilizalasa, mert a lecsukas mar hiba nelkul futott, de a tray ikonrol visszanyitas meg mindig bezarta az appot.
- Modositott fajlok: `src/tecsoo_letolto/gui/main_window.py`; `src/tecsoo_letolto/gui/tray.py`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `.venv-build\Scripts\python.exe -m compileall -q src\tecsoo_letolto`; `.venv-build\Scripts\python.exe -m pytest`; `scripts\build_release.bat`.
- Eredmeny: A Win32 callback mar csak visszanyitasi jelzot allit. A tenyleges Tk restore es tray hook eltavolitas a Tk main loop polling agaban fut, hogy ne callback kozben tortenjen Tk muvelet vagy hook bontas. Teljes teszt: `73 passed`; release build es self-check zold. ZIP artifact ujrageneralva.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: kezi GUI smoke ujraellenorzes a friss builddel.

## 2026-06-24 21:30 +02:00

- Cel: A release GUI inditasakor ne nyiljon kulon CMD ablak.
- Modositott fajlok: `scripts/tools/build-release.ps1`; `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Futtatott parancsok: `scripts\build_release.bat`; `.venv-build\Scripts\python.exe -c "import pefile; ..."`; `scripts\verify_release.bat`; `git diff --check`.
- Eredmeny: A PyInstaller build `--windowed` modra valtott, es a logban mar `runw.exe` bootloader szerepel. A kesz `release\TecsoLetolto\TecsoLetolto.exe` PE subsystem erteke `2` (Windows GUI), tehat nem console executable. Release self-check zold, ZIP artifact ujrageneralva.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: kezi GUI smoke Explorerbol inditva: csak GUI jelenjen meg, CMD ablak nelkul.

## 2026-06-24 21:44 +02:00

- Cel: Ovatos repo takaritas a mai ujratervezes utan.
- Modositott fajlok: `scripts/clean_repo.bat`; `docs/codex-tasks/repo_cleanup_report.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Torolt lokalis mappak: `.agents/`; `.codex/`; `.serena/`.
- Megtartott lokalis kimenetek: `.venv-build/`; `vendor/`; `release/`; `artifacts/`.
- Futtatott parancsok: `git status --short --branch --ignored`; `git clean -ndX`; `git clean -ndx -e .venv-build/ -e vendor/ -e release/ -e artifacts/ -e .serena/`; explicit PowerShell path-ellenorzott `Remove-Item`; `scripts\clean_repo.bat`.
- Eredmeny: Ures lokalis segedmappak es Serena lokalis index/cache torolve. A cleanup script mar torli a Python cache-t, `.pytest_cache`-t, `*.egg-info` mappakat, PyInstaller `build/`, `dist/`, `TecsoLetolto.spec` kozteseket es `.serena/` cache-t, de nem torli a friss release/vendor/artifact payloadot.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: commit/review dontes.

## 2026-06-24 21:52 +02:00

- Cel: A sikeres kezi GUI smoke utan az ujratervezesi terv lezarasa commit/push elott.
- Modositott fajlok: `docs/codex-tasks/done/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `docs/codex-tasks/done/vendor-and-local-media-decision-2026-06-24.md`; `STATE.md`; `docs/CHANGELOG.dev.md`.
- Mozgatott fajlok: `docs/codex-tasks/pending/active/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md` -> `docs/codex-tasks/done/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`; `docs/codex-tasks/pending/not-started/vendor-and-local-media-decision-2026-06-24.md` -> `docs/codex-tasks/done/vendor-and-local-media-decision-2026-06-24.md`.
- Eredmeny: A terv statusza `done`, nincs fennmarado blocker; kovetkezo lepes a pre-commit validacio, commit es push.
- Verzio: marad `0.1.0-dev`.
- Nyitott follow-up: nincs a mai tervhez.
