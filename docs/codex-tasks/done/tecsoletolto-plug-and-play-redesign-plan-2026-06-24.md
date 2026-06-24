# Status

- Allapot: done / ujratervezesi megvalositas lezárva.
- Aktualis repo-kapcsolat: az uj app `src/tecsoo_letolto/` package alapon epul, PyInstaller one-folder release mappaval. A regi aprilisi monolit Python fajlok, BAT inditok, regi installer scriptek, regi `requirements.txt`, regi `.venv` es repo alatti `downloads/` mar torolve lettek.
- Forrasanyag: `docs/ujratervezés.md`, jelenlegi repo audit, valamint az `email-header-analyzer` dokumentacio- es tervkovetesi mintaja: aktiv tervek `docs/codex-tasks/pending/active/`, lezart tervek `docs/codex-tasks/done/`, allapot `STATE.md`, fejlesztoi naplo `docs/CHANGELOG.dev.md`.
- Cel: olyan Windows 10/11 x64 portable alkalmazas, amelyhez a felhasznalonak nem kell Python, pip, FFmpeg, yt-dlp vagy parancssor.
- Fontos hatar: a `release/TecsoLetolto/` mappaba csak a kesz futtathato program es a runtime payload kerulhet; fejlesztoi forras, teszt, cache, naplo, user media vagy build szemet nem.
- Kesz resz: reszletes ujratervezesi terv es repo-kovetesi konvencio rogzult ebben a fajlban.
- Kesz resz: elso implementacios szelet bekerult: `pyproject.toml`, `src/tecsoo_letolto/` package scaffold, `core/errors.py`, `core/filename_policy.py`, `core/paths.py`, valamint `tests/core/test_filename_policy.py` es `tests/core/test_paths.py`.
- Kesz resz: Python 3.12 alapu `.venv-build` validacioval `python -m pytest tests\core` zold: `19 passed`; `python -m tecsoo_letolto --version` OK (`0.1.0-dev`).
- Kesz resz: masodik implementacios szelet bekerult: `core/error_mapping.py`, `utils/redaction.py`, `utils/subprocess_runner.py`, `core/media_info.py`, `core/progress.py`, `services/ffmpeg_service.py`, `services/ytdlp_service.py`, valamint ezek unit tesztjeinek elso kore. Teljes eddigi validacio: `42 passed`, `git diff --check` tiszta.
- Kesz resz: support report, logging setup es self-check alap bekerult. Teljes eddigi validacio: `49 passed`, version smoke OK, `git diff --check` tiszta. A valos `--self-check` jelenleg fut, de vendor `yt-dlp.exe` es FFmpeg hiany miatt FAIL statuszt ad, ami a kesobbi vendor/build szelet nyitott feladata.
- Kesz resz: GUI view-model es egyablakos Tk main window scaffold bekerult a scope-korlatozott mezokkel es gombokkal. Normal app entrypoint mar a GUI-t inditja, `--version` es `--self-check` parancs megmaradt. Teljes eddigi validacio: `55 passed`.
- Kesz resz: `core/download_manager.py` bekerult szinkron backend futtatasi alappal: output path valasztas, vendor FFmpeg/yt-dlp ellenorzes, yt-dlp argumentumepites es hibatérkép. Teljes eddigi validacio: `59 passed`.
- Kesz resz: GUI `Letöltés indítása` gomb worker threaden keresztul a `DownloadManager`-t hivja, es a Tk frissitesek visszaternek a main threadre. Teljes eddigi validacio: `59 passed`.
- Kesz resz: `services/update_service.py` bekerult kezi yt-dlp frissiteshez: aktualis/verzio lekerdezes, latest release tag olvasas, letoltes, futtathatosag ellenorzes, backup, rollback es nem yt-dlp target vedelme. Teljes eddigi validacio: `65 passed`.
- Kesz resz: alap dokumentacios fajlok es script vazak bekerultek: `docs/USER_GUIDE.md`, `docs/SUPPORT.md`, `docs/BUILD.md`, `docs/RELEASE.md`, `docs/RELEASE_TEST_CHECKLIST.md`, `docs/THIRD_PARTY_LICENSES.md`, `docs/CHANGELOG.md`, `scripts/build_dev.bat`, `scripts/build_release.bat`, `scripts/verify_release.bat`, `scripts/clean_repo.bat`, valamint `docs/codex-tasks/repo_cleanup_report.md`. `scripts\build_dev.bat` zold, `65 passed`.
- Eldolt vendor dontes: `yt-dlp.exe` a hivatalos `yt-dlp/yt-dlp` GitHub stable latest release-bol jon, SHA-256 ellenorzessel, es nem commitolhato a forrasrepoba. Rogzitve: `docs/codex-tasks/done/vendor-and-local-media-decision-2026-06-24.md`.
- Reszben eldolt vendor dontes: FFmpeg/FFprobe a BtbN/FFmpeg-Builds `ffmpeg-master-latest-win64-lgpl.zip` assetbol jon; GPL/full/nonfree fallback nincs emberi dontes nelkul.
- Eldolt repo-takaritasi dontes: a helyi `downloads/` media mappa teszt soran letoltott anyagai torolhetok; a mappa torolve lett.
- Kesz resz: PyInstaller one-folder release build bekerult `scripts/build_release.bat` alatt, sajat vendor `yt-dlp` es FFmpeg payload bemasolassal, manifesttel, ZIP artifacttal es `scripts\verify_release.bat` self-check validacioval. Validacio: `68 passed`; release `--version` OK; release `--self-check` OK.
- Kesz resz: regi aprilisi futtatasi/build utvonalak es lokalis maradekok torolve: `letolto.py`, `letolto_gui.py`, regi BAT-ok, regi installer scriptek, regi `requirements.txt`, regi `.venv`, repo `downloads/`.
- Kesz resz: process-szintu download streaming bekerult. A `DownloadManager` mar soronkent olvassa a yt-dlp kimenetet, `ProgressEvent` esemenyeket kuld, es `CancelToken` alapjan megszakitja a futast. A GUI cancel gomb most mar tenyleges megszakitasi kerest ad a backendnek.
- Kesz resz: GUI yt-dlp frissites ellenorzes es jovahagyott frissites bekerult. A gomb lekéri a jelenlegi es latest verziot, megerositest ker, majd csak `vendor/yt-dlp/yt-dlp.exe` fajlt cserel, SHA-256 ellenorzessel es rollback alappal.
- Kesz resz: kezi GUI smoke visszajelzes alapjan javitva lett a placeholder sugo, a hianyos support report runtime adatfeltoltese, es a sima minimalizalas helyett Windows ertesitesi teruletre rejtes.
- Kesz resz: tray smoke hiba javitva: a Windows window procedure callback 64 bites pointertipusai es az eredeti wndproc visszaallitasa bekerult, hogy az `int too long to convert` callback hiba ne zarja be az appot.
- Kesz resz: tray restore flow stabilizalva: a Win32 callback mar csak visszanyitasi jelzot allit, a tenyleges Tk `deiconify`/`lift` es tray hook bontas a Tk main loop 200 ms-os polling agaban fut.
- Kesz resz: a release build PyInstaller `--windowed` modra valtott, igy a kesz GUI inditasakor nem nyilik kulon CMD ablak. PE subsystem ellenorzes: `2` (Windows GUI).
- Kesz resz: kezi GUI smoke alapján a friss windowed build jo lett: inditaskor csak a GUI latszik, a notification-area lecsukas/visszanyitas nem omlik.
- Lezaras: 2026-06-24, commit/push elott.

## 0.X. Szigorú scope-korlátok Codex-agent számára

A fejlesztés célja egy stabil, egyszerű, laikusbarát portable Windows alkalmazás. Tilos a feladatot általános letöltőplatformmá, komplex biztonsági rendszerrel ellátott updater keretrendszerré vagy túl sok opciót tartalmazó haladó eszközzé bővíteni.

### Kötelező scope

Az első működő release kizárólag ezeket tudja:

1. URL beillesztése.
2. Mentési mappa kiválasztása.
3. Opcionális fájlnév megadása.
4. Csak hang letöltése.
5. Videó + hang letöltése.
6. Egyszerű minőségválasztás: Normál / Jó / Legjobb elérhető.
7. Egyszerű hangformátum-választás: mp3 / m4a / opus / wav.
8. Egyszerű videóformátum-választás: mp4 / mkv.
9. Letöltés indítása.
10. Letöltés megszakítása.
11. Mezők törlése.
12. Sikeres letöltés után mappa megnyitása.
13. Sima Windows tálcára minimalizálás.
14. Offline magyar súgó.
15. Support jelentés előnézete.
16. Support jelentés küldése a felhasználó saját levelezőprogramjával.
17. yt-dlp verzió ellenőrzése.
18. yt-dlp.exe kézi, felhasználó által jóváhagyott frissítése.
19. Névjegy ablak.
20. Self-check mód.
21. Release build ellenőrzés.
22. Repo-takarítás.

### Kifejezetten tilos az első release-ben

Nem készülhet:

1. System tray háttéralkalmazás.
2. Háttérben futó update service.
3. Automatikus, felhasználói jóváhagyás nélküli frissítés.
4. Az alkalmazás saját EXE-jének belső frissítése.
5. Cookie import.
6. Böngésző cookie olvasás.
7. Login kezelés.
8. Proxy konfigurációs panel.
9. User-agent szerkesztő.
10. Haladó yt-dlp kapcsolók GUI-n.
11. Tömeges letöltési lista.
12. Playlist letöltés.
13. Felhőszinkron.
14. Adatbázis.
15. Felhasználói fiókrendszer.
16. Beépített SMTP küldés.
17. SMTP jelszó vagy token tárolása.
18. DRM, hozzáférési vagy előfizetéses korlátozás megkerülése.
19. Bonyolult jogosultságkezelés.
20. Telemetria.
21. Automatikus hibajelentés-küldés.

Ha valamelyik extra funkció szükségesnek tűnik, azt nem szabad implementálni. Helyette `TODO_FUTURE.md` vagy `docs/codex-tasks/pending/not-started/` alá kell felírni rövid indoklással.

### GUI scope-korlát

A GUI legyen egyablakos.

Nem lehet:

* több főablak,
* haladó beállítások panel,
* plugin rendszer,
* parancssori opciókat tükröző technikai felület,
* túlzsúfolt lognézet.

A főablak tartalmazza a szükséges mezőket és gombokat, de ne adjon hozzá olyan opciót, amelyet a felhasználói követelmény nem kér.

A 2026-06-24-i kezi GUI teszt dontese alapjan a korabbi “tálcára minimalizálás” szoveg helyett az “értesítési területre” rejtés a cel: az ablak tunjon el a fo tálcáról, es a jobb also Windows notification area ikonjarol legyen visszanyithato. Nem jelent háttérben futó szolgáltatást.

### yt-dlp frissítés scope-korlát

A belső frissítés kizárólag a következő fájlra vonatkozhat:

```text
vendor/yt-dlp/yt-dlp.exe
```

Nem frissítheti:

* a fő alkalmazás EXE-jét,
* FFmpeg-et,
* Python runtime-ot,
* PyInstaller payloadot,
* dokumentációt,
* bármilyen más komponenst.

A frissítés csak kézi lehet:

1. felhasználó megnyomja a “Frissítés ellenőrzése” gombot;
2. program megmutatja az aktuális és elérhető verziót;
3. felhasználó jóváhagyja;
4. program letölti az új `yt-dlp.exe` fájlt;
5. program ellenőrzi, hogy az új fájl fut-e;
6. sikertelenség esetén visszaáll az előző példányra.

Nincs automatikus háttérellenőrzés.

### Support scope-korlát

A Support funkció nem küldhet közvetlen SMTP-vel.

A működés:

1. hibajelentés összeállítása;
2. hibajelentés előnézete;
3. felhasználó ellenőrzi;
4. program megnyitja az alapértelmezett levelezőprogramot `mailto:` linkkel;
5. ha a `mailto:` túl hosszú vagy sikertelen, a program mentse a hibajelentést `.txt` fájlba, és kínáljon “Másolás vágólapra” lehetőséget.

A hibajelentés alapértelmezés szerint ne tartalmazza a teljes URL-t, cookie-t, tokent, jelszót, teljes környezeti változó listát vagy érzékeny helyi útvonalat.

### Mentési mappa szabály

Ha a felhasználó nem ad meg mentési mappát, a program elsődlegesen a Windows hivatalos Letöltések ismert mappáját próbálja használni.

Fallback:

```text
%USERPROFILE%\Downloads
```

Nem használható alapértelmezett mentési helyként:

* a program mappája,
* a repo gyökere,
* `release/TecsoLetolto/`,
* `downloads/` a repo alatt.

### Régi fájlok végső sorsa

A régi monolit fájlok és BAT indítók csak átmenetileg maradhatnak meg referencia célból.

A végső állapotban nem maradhat két párhuzamos futtatási útvonal.

Az új release sikeres ellenőrzése után törlendő vagy dokumentáltan kiváltandó:

* régi `letolto.py`;
* régi `letolto_gui.py`;
* régi `run.bat`;
* régi `run_gui.bat`;
* régi debug BAT;
* régi PyInstaller BAT;
* régi installer payload maradék;
* régi lokális log;
* régi downloads mappa;
* `__pycache__`;
* `.pyc`;
* `.spec`;
* `.venv`;
* bármilyen buildszemét.

Ha valamelyik régi fájl tartalma hasznos, azt át kell emelni az új modulokba vagy dokumentációs kivonatként kell menteni. Régi működő programlogika nem maradhat a repo gyökerében.

### Vendor komponensek szabálya

A forrásrepóba alapértelmezés szerint ne kerüljenek nagy bináris runtime fájlok.

A build folyamatnak egyértelműen kezelnie kell, honnan származnak:

* `yt-dlp.exe`;
* `ffmpeg.exe`;
* `ffprobe.exe`.

Elfogadott megoldások:

1. dokumentált `scripts/fetch_vendor_tools.bat`;
2. `yt-dlp.exe` eseteben dokumentalt fetch script a hivatalos GitHub release-bol;
3. FFmpeg eseteben dokumentalt fetch script, amely csak a BtbN `ffmpeg-master-latest-win64-lgpl.zip` assetet fogadja el;
4. build előtti ellenőrzés, amely érthető hibát ad, ha a szükséges fájlok hiányoznak.

A release mappába csak ellenőrzött vendor fájl kerülhet.

### Tesztelési korlát

Az első release-ben nem kell automata GUI screenshot teszt, nem kell end-to-end valódi YouTube letöltési teszt CI alatt, és nem kell komplex biztonsági audit framework.

Kötelező viszont:

* unit teszt a fájlnévkezelésre;
* unit teszt az útvonalkezelésre;
* unit teszt a hibaüzenet-mappingre;
* unit teszt a support report redakcióra;
* unit teszt a yt-dlp argumentumépítésre;
* self-check;
* release mappa ellenőrzése;
* kézi GUI smoke checklist.

### Magyar ékezetes útvonalak

Tesztelni kell, hogy a program működik ékezetes felhasználói útvonalakkal is.

Példák:

```text
C:\Users\Bíró Attila\Downloads
C:\Users\Teszt Elek\Letöltések
```

A program minden fájlműveletnél Unicode-kompatibilis útvonalkezelést használjon.

### Döntési szabály bizonytalanság esetén

Ha Codex-agent nem biztos valamiben, nem implementálhat saját nagyobb megoldást.

Helyette:

1. hagyjon rövid `TODO_DECISION` megjegyzést;
2. dokumentálja a kérdést a megfelelő `docs/codex-tasks/pending/not-started/` fájlban;
3. a jelenlegi release scope-ot ne bővítse.

# 0. Vezeto dontesek

## 0.1. Atvett repo-fegyelem

1. Uj vagy aktiv terv: `docs/codex-tasks/pending/active/`.
2. Meg nem kezdett, de konkret jovobeli terv: `docs/codex-tasks/pending/not-started/`.
3. Hatteranyag vagy regi prompt: `docs/codex-tasks/pending/reference/`.
4. Lezart terv: `docs/codex-tasks/done/`.
5. Minden erdemi fejlesztes utan frissuljon:
   - `STATE.md`;
   - `docs/CHANGELOG.dev.md`;
   - az aktiv terv statuszblokkja.
6. Csak docs/terv valtozasnal nincs verzio bump.
7. User-facing viselkedes, build payload vagy runtime szerzodes valtozasnal legyen verzio bump.

## 0.2. Vegleges termeknev

- Python package: `tecsoo_letolto`
- Lathato appnev: `TecsoLetolto`
- EXE: `TecsoLetolto.exe`
- Portable mappa: `release/TecsoLetolto/`
- Log root: `%LOCALAPPDATA%\TecsoLetolto\logs\`
- App data root: `%LOCALAPPDATA%\TecsoLetolto\`

## 0.3. Technologiai alap

- Nyelv: Python 3.12, ha nincs kesobbi projekt-dontes masrol.
- GUI: maradhat `tkinter` / `ttk`, mert keves dependency, jol csomagolhato, es eleg ehhez a celhoz.
- Letolto backend: kulso `vendor/yt-dlp/yt-dlp.exe` subprocess hivas az elso release celja.
- FFmpeg: `vendor/ffmpeg/bin/ffmpeg.exe` es `vendor/ffmpeg/bin/ffprobe.exe`.
- Build: PyInstaller one-folder release az elso stabil cel; installer kesobb opcionális.

# 1. Cel repo-struktura

```text
tecsoo-letolto/
├─ src/
│  └─ tecsoo_letolto/
│     ├─ __init__.py
│     ├─ __main__.py
│     ├─ app.py
│     ├─ version.py
│     ├─ gui/
│     │  ├─ __init__.py
│     │  ├─ main_window.py
│     │  ├─ dialogs.py
│     │  ├─ view_model.py
│     │  └─ widgets.py
│     ├─ core/
│     │  ├─ __init__.py
│     │  ├─ download_manager.py
│     │  ├─ errors.py
│     │  ├─ error_mapping.py
│     │  ├─ filename_policy.py
│     │  ├─ media_info.py
│     │  ├─ paths.py
│     │  ├─ progress.py
│     │  ├─ settings.py
│     │  └─ support_report.py
│     ├─ services/
│     │  ├─ __init__.py
│     │  ├─ ffmpeg_service.py
│     │  ├─ ytdlp_service.py
│     │  └─ update_service.py
│     ├─ utils/
│     │  ├─ __init__.py
│     │  ├─ logging_setup.py
│     │  ├─ redaction.py
│     │  └─ subprocess_runner.py
│     └─ resources/
│        ├─ help/
│        └─ app.ico
├─ tests/
│  ├─ core/
│  ├─ services/
│  └─ utils/
├─ docs/
│  ├─ USER_GUIDE.md
│  ├─ SUPPORT.md
│  ├─ BUILD.md
│  ├─ RELEASE.md
│  ├─ RELEASE_TEST_CHECKLIST.md
│  ├─ THIRD_PARTY_LICENSES.md
│  ├─ CHANGELOG.md
│  ├─ CHANGELOG.dev.md
│  └─ codex-tasks/
├─ scripts/
│  ├─ build_dev.bat
│  ├─ build_release.bat
│  ├─ clean_repo.bat
│  ├─ verify_release.bat
│  └─ tools/
├─ release/
│  └─ TecsoLetolto/
├─ artifacts/
├─ vendor/
│  ├─ yt-dlp/
│  └─ ffmpeg/
├─ pyproject.toml
├─ README.md
├─ AGENTS.md
├─ STATE.md
├─ .gitignore
└─ LICENSE
```

# 2. Implementacios sorrend

## 2.1. Szelet A: repo-alap es kovetes

Statusz 2026-06-24 18:18 +02:00:

- Reszben kesz: `pyproject.toml`, package scaffold es test scaffold letrejott.
- Kesz: `.gitignore` bovult `.venv-build/`, `.venv-dev/`, `venv/`, `env/` kizarassal.
- Nyitott: `docs/CHANGELOG.md`, kesobbi build/release script es teljes docs skeleton.

1. Letrehozando mappak:
   - `src/tecsoo_letolto/`;
   - `tests/`;
   - `docs/codex-tasks/pending/active/`;
   - `docs/codex-tasks/done/`;
   - `scripts/`.
2. Letrehozando vagy frissitendo fajlok:
   - `pyproject.toml`;
   - `docs/CHANGELOG.dev.md`;
   - `docs/CHANGELOG.md`;
   - `.gitignore`;
   - `STATE.md`.
3. `pyproject.toml` minimum:
   - `[project] name = "tecsoo-letolto"`;
   - `version = "0.1.0-dev"`;
   - `requires-python = ">=3.12"`;
   - runtime dependencies: minimalis, lehetoseg szerint ures `dependencies = []`;
   - dev/test dependencies: `pytest` csak optional `test` extra alatt;
   - build dependencies: `pyinstaller` csak optional `build` extra alatt.
4. Dontes: a repo source-ban ne legyen runtime `vendor` binaris commitolva, hacsak kulon release-policy nem dont maskepp.
5. Build output:
   - `release/` es `artifacts/` alapbol ignored;
   - release ZIP/installer GitHub Release artifact legyen, ne forraskod commit.

## 2.2. Szelet B: core modulok kimentese a monolitbol

Statusz 2026-06-24 18:18 +02:00:

- Kesz: `core/errors.py`, `core/filename_policy.py`, `core/paths.py`.
- Kesz: `tests/core/test_filename_policy.py` es `tests/core/test_paths.py`.
- Validacio: `.venv-build\Scripts\python.exe -m pytest tests\core` -> `19 passed`.
- Nyitott ebbol a szeletbol: `core/error_mapping.py`.

### `src/tecsoo_letolto/core/paths.py`

Feladat:

```python
from pathlib import Path

APP_NAME = "TecsoLetolto"

def user_downloads_dir() -> Path: ...
def default_output_dir() -> Path: ...
def local_app_data_dir() -> Path: ...
def logs_dir() -> Path: ...
def app_base_dir() -> Path: ...
def packaged_resource_dir() -> Path: ...
def release_vendor_dir() -> Path: ...
def ensure_writable_dir(path: Path) -> None: ...
```

Reszletek:

1. `user_downloads_dir()` Windows alatt `Path.home() / "Downloads"`.
2. `default_output_dir()` ne a program mappaja legyen, hanem a felhasznalo Downloads mappaja.
3. `app_base_dir()` PyInstaller alatt `Path(sys.executable).parent`, source futasnal repo vagy package root.
4. `ensure_writable_dir()`:
   - `mkdir(parents=True, exist_ok=True)`;
   - kis proba fajlt irjon es toroljon;
   - hiba eseten `OutputDirectoryError`.

Teszt:

- `tests/core/test_paths.py`
- mockolt `Path.home`;
- nem letezo mappa letrehozasa temp alatt;
- nem irhato mappa teszt csak platform-safe modon, vagy skip.

### `src/tecsoo_letolto/core/filename_policy.py`

Feladat:

```python
WINDOWS_ILLEGAL_CHARS = ...
WINDOWS_RESERVED_NAMES = ...

def sanitize_filename_base(value: str, fallback: str = "letoltes") -> str: ...
def build_default_filename(title: str | None, extension: str, now: datetime | None = None) -> str: ...
def split_name_and_extension(filename: str) -> tuple[str, str]: ...
def next_available_path(directory: Path, filename: str) -> Path: ...
```

Sor-szintu viselkedes:

1. Cserelje `_` jelre: `< > : " / \ | ? *` es control karakterek.
2. `strip()`, majd jobb oldalon pont es space torles.
3. Ures nev fallback: `letoltes`.
4. Reserved nev:
   - `CON`, `PRN`, `AUX`, `NUL`, `COM1..COM9`, `LPT1..LPT9`;
   - kis/nagybetu fuggetlen;
   - eredmeny: `CON_`.
5. Max base hossz: 180-200 karakter, extension nelkul.
6. `build_default_filename(None, "mp3")` forma:
   - `letoltes_YYYY-MM-DD_HHMMSS.mp3`
7. `build_default_filename("Cim", "mp3")` forma:
   - `Cim_YYYY-MM-DD.mp3`
8. `next_available_path()`:
   - ha nincs konfliktus, eredeti path;
   - ha van: `_01`, `_02`, ... `_99`;
   - 100 utan `FilenameConflictError`.

Teszt:

- illegal chars;
- reserved names;
- ponttal vegzodo nev;
- ures nev;
- hosszu nev;
- utkozes `_01`, `_02`.

### `src/tecsoo_letolto/core/errors.py`

Feladat:

```python
class TecsoLetoltoError(Exception): ...
class InvalidUrlError(TecsoLetoltoError): ...
class UnsupportedUrlError(TecsoLetoltoError): ...
class NetworkError(TecsoLetoltoError): ...
class RestrictedContentError(TecsoLetoltoError): ...
class DownloadCancelledError(TecsoLetoltoError): ...
class OutputDirectoryError(TecsoLetoltoError): ...
class NotEnoughSpaceError(TecsoLetoltoError): ...
class FfmpegError(TecsoLetoltoError): ...
class YtDlpError(TecsoLetoltoError): ...
class ToolMissingError(TecsoLetoltoError): ...
class ToolUpdateError(TecsoLetoltoError): ...
```

Minden error kapjon:

- `category: str`;
- `user_message: str`;
- `technical_detail: str | None`;
- `cause: Exception | None`.

### `src/tecsoo_letolto/core/error_mapping.py`

Feladat:

```python
def map_subprocess_failure(tool: str, returncode: int, stdout: str, stderr: str) -> TecsoLetoltoError: ...
def map_exception(exc: Exception) -> TecsoLetoltoError: ...
def user_error_text(error: TecsoLetoltoError) -> str: ...
```

Mapping:

1. `HTTP Error 416` -> retry policy kezeli; ha vegul bukik: `YtDlpError`.
2. `Unsupported URL` -> `UnsupportedUrlError`.
3. `Private video`, `Sign in`, `age-restricted`, `members-only` -> `RestrictedContentError`.
4. DNS/socket/timeout -> `NetworkError`.
5. permission denied / access is denied -> `OutputDirectoryError`.
6. no space left -> `NotEnoughSpaceError`.
7. ffmpeg returncode != 0 -> `FfmpegError`.

Teszt:

- minden kategoriara legalabb egy synthetic stderr minta;
- user szoveg magyar, technikai resz kulon.

## 2.3. Szelet C: tool es subprocess szolgaltatasok

Statusz 2026-06-24 18:21 +02:00:

- Kesz: `utils/subprocess_runner.py`.
- Kesz: `services/ffmpeg_service.py` vendor FFmpeg/ffprobe keresesi es ellenorzesi alap.
- Kesz: `services/ytdlp_service.py` vendor `yt-dlp.exe` keresesi es audio/video argumentumepitesi alap.
- Kesz: `tests/utils/test_subprocess_runner.py`, `tests/services/test_ffmpeg_service.py`, `tests/services/test_ytdlp_service.py`.
- Validacio: `.venv-build\Scripts\python.exe -m pytest` -> `42 passed`.

### `src/tecsoo_letolto/utils/subprocess_runner.py`

Feladat:

```python
@dataclass(frozen=True)
class ProcessResult:
    args: list[str]
    returncode: int
    stdout: str
    stderr: str

class RunningProcess:
    def cancel(self) -> None: ...

def run_checked(args: list[str], timeout: int = 30, cwd: Path | None = None) -> ProcessResult: ...
def start_streaming(args: list[str], cwd: Path | None = None) -> RunningProcess: ...
```

Windows-szabaly:

- `creationflags=subprocess.CREATE_NO_WINDOW`, ha elerheto.
- Soha ne `shell=True`, ha nem muszaj.
- Logba redaktalt arglista menjen.

### `src/tecsoo_letolto/services/ffmpeg_service.py`

Feladat:

```python
@dataclass(frozen=True)
class FfmpegTools:
    ffmpeg: Path
    ffprobe: Path
    version: str

def find_packaged_ffmpeg(base_dir: Path | None = None) -> FfmpegTools: ...
def check_ffmpeg(ffmpeg: Path, ffprobe: Path) -> FfmpegTools: ...
```

Keresesi sorrend:

1. `app_base_dir()/vendor/ffmpeg/bin/ffmpeg.exe`
2. `app_base_dir()/ffmpeg/bin/ffmpeg.exe` csak backward compatibility miatt, kesobb torolheto.
3. Dev fallback csak explicit `TECSOLETOLTO_DEV_FFMPEG_DIR`, nem beégetett `E:\...`.

Eltavolitando regi logika:

- `DEFAULT_FFMPEG_DIR = r"E:\ffmpeg-..."` teljes torles.
- `FFMPEG_DIR` env csak dev override lehet, user-facing portable release ne erre epuljon.

Teszt:

- temp vendor fa `ffmpeg.exe` es `ffprobe.exe` dummy fajlokkal;
- subprocess runner mock version kimenettel;
- hianyzo `ffprobe.exe` -> `ToolMissingError`.

### `src/tecsoo_letolto/services/ytdlp_service.py`

Feladat:

```python
@dataclass(frozen=True)
class YtDlpTool:
    executable: Path
    version: str

@dataclass(frozen=True)
class DownloadRequest:
    url: str
    output_dir: Path
    filename_base: str | None
    mode: Literal["audio", "video"]
    audio_format: Literal["mp3", "m4a", "opus", "wav"]
    video_format: Literal["mp4", "mkv"]
    quality: Literal["normal", "good", "best"]

def find_packaged_ytdlp(base_dir: Path | None = None) -> YtDlpTool: ...
def get_media_info(tool: YtDlpTool, url: str) -> MediaInfo: ...
def build_ytdlp_args(request: DownloadRequest, tools: RuntimeTools, output_path: Path) -> list[str]: ...
def run_download(request: DownloadRequest, progress: ProgressSink, cancel_token: CancelToken) -> DownloadResult: ...
```

`build_ytdlp_args()` alapelvek:

1. `vendor/yt-dlp/yt-dlp.exe` hivas.
2. `--ffmpeg-location vendor/ffmpeg/bin`.
3. `--no-playlist` alapbol.
4. `--newline` progress parsinghoz.
5. `--no-overwrites`.
6. Audio:
   - `-f bestaudio/best`;
   - `--extract-audio`;
   - `--audio-format mp3|m4a|opus|wav`;
   - `--audio-quality` minoseghez mapelve.
7. Video:
   - `-f` quality map alapjan:
     - normal: `bv*[height<=720]+ba/best[height<=720]/best`;
     - good: `bv*[height<=1080]+ba/best[height<=1080]/best`;
     - best: `bv*+ba/best`;
   - `--merge-output-format mp4|mkv`.
8. Kimenet:
   - `-o <safe target template>`;
   - ne legyen raw title kozvetlenul filename-kent.

416 fallback:

- A mostani `_download_with_416_fallback` koncepcio megtarthato, de subprocess modban:
  1. elso futas resume engedelyezve;
  2. ha stderr tartalmaz `HTTP Error 416` vagy `Requested range not satisfiable`;
  3. kapcsolodo `.part` fajlok celzott torlese;
  4. retry `--no-continue` vagy azzal ekvivalens opcioval.

Teszt:

- arg builder snapshot jellegu assert;
- quality map;
- audio/video mod;
- 416 stderr -> retry policy unit test mockolt runnerrel.

## 2.4. Szelet D: media info es progress

### `src/tecsoo_letolto/core/media_info.py`

```python
@dataclass(frozen=True)
class MediaInfo:
    title: str | None
    webpage_url: str
    extractor: str | None
    duration_seconds: int | None
    id: str | None
```

Feladat:

- `yt-dlp --dump-json --no-playlist <url>` kimenetbol parse.
- URL-t nem kell teljesen logolni; support reportban redaktalni.

### `src/tecsoo_letolto/core/progress.py`

```python
@dataclass(frozen=True)
class ProgressEvent:
    phase: Literal["preparing", "downloading", "postprocessing", "done", "error"]
    percent: float | None
    message: str

class ProgressSink(Protocol):
    def publish(self, event: ProgressEvent) -> None: ...

class CancelToken:
    def cancel(self) -> None: ...
    def is_cancelled(self) -> bool: ...
```

Progress parser:

- yt-dlp sorokbol `12.3%`, ETA, speed kinyerese best-effort.
- Ha nincs percent, akkor indeterminate progress.

Teszt:

- `[download]  12.3% of ... at ... ETA ...`;
- `[ExtractAudio]`;
- `[Merger]`.

## 2.4.B. Download manager backend

Statusz 2026-06-24 18:27 +02:00:

- Kesz: `core/download_manager.py`.
- Kesz: `DownloadManager.run()` ellenorzi az output mappa irhatosagat, vendor FFmpeg/yt-dlp jelenletet, kivalasztja az output pathot, majd futtatja a `yt-dlp` parancsot.
- Kesz: hibas `yt-dlp` eredmeny `map_subprocess_failure()` alapu domain hibava alakul.
- Kesz: `tests/core/test_download_manager.py`.
- Validacio: `.venv-build\Scripts\python.exe -m pytest` -> `59 passed`.
- Kesz: cancel/progress streaming es GUI thread bekotes.

## 2.5. Szelet E: GUI ujraszervezes

Statusz 2026-06-24 18:26 +02:00:

- Kesz: `gui/view_model.py` validacio es `DownloadRequest` konverzio.
- Kesz: `gui/main_window.py` egyablakos Tk scaffold a kert mezokkel es gombokkal.
- Kesz: `app.py` normal modban a GUI-t inditja; `--version` es `--self-check` tovabbra is CLI parancs.
- Kesz: `Letöltés indítása` backend worker threaden hivja a `DownloadManager`-t, hiba eseten `user_error_text()` magyar uzenetet mutat.
- Kesz: `tests/gui/test_view_model.py`.
- Validacio: `.venv-build\Scripts\python.exe -m pytest` -> `55 passed`.
- Validacio 2026-06-24 18:29 +02:00: `.venv-build\Scripts\python.exe -m pytest` -> `59 passed`.
- Kesz: process-szintu cancel es progress streaming.

### `src/tecsoo_letolto/gui/view_model.py`

```python
@dataclass
class DownloadFormState:
    url: str = ""
    output_dir: str = ""
    filename: str = ""
    mode: str = "audio"
    audio_format: str = "mp3"
    video_format: str = "mp4"
    quality: str = "good"

def validate_form(state: DownloadFormState) -> list[str]: ...
def to_download_request(state: DownloadFormState) -> DownloadRequest: ...
```

Validation:

1. URL nem ures.
2. URL `http://` vagy `https://`.
3. Output ures lehet, ekkor default Downloads.
4. Filename opcionális, de ha van, menjen `sanitize_filename_base`.
5. Tiltott funkciokhoz nincs mező:
   - cookie import;
   - login;
   - DRM/region bypass.

### `src/tecsoo_letolto/gui/main_window.py`

Fokontrollok:

1. Link mező + `Beillesztés`.
2. Mentési mappa + `Tallózás`.
3. Fájlnév + opcionális placeholder.
4. Mod valaszto: `Csak hang`, `Videó + hang`.
5. Hangformatum: `mp3`, `m4a`, `opus`, `wav`.
6. Videoformatum: `mp4`, `mkv`.
7. Minoseg: `Normál`, `Jó`, `Legjobb elérhető`.
8. `Letöltés indítása`.
9. `Letöltés megszakítása`.
10. `Mezők törlése`.
11. `Mappa megnyitása`.
12. `Tálcára minimalizálás`.
13. `Súgó`.
14. `Support`.
15. `Névjegy`.
16. `Kilépés`.

GUI sor-szintu allapotlogika:

- `set_running(True)`:
  - start disabled;
  - cancel enabled;
  - URL/output/name/options disabled;
  - progress indeterminate vagy percent mod.
- `set_running(False)`:
  - start enabled;
  - cancel disabled;
  - options enabled;
  - status: `Készen áll.` vagy utolso eredmeny.
- Worker thread:
  - ne nyuljon kozvetlen Tk widgethez;
  - `root.after(0, ...)` queue-val frissitsen.
- Hiba:
  - `error_mapping.user_error_text`;
  - reszletes log fajlba.

### `src/tecsoo_letolto/gui/dialogs.py`

Dialogok:

- `show_help()`: offline HTML/Markdown help.
- `show_about(runtime_versions)`.
- `show_support_preview(report_text)`.
- `confirm_ytdlp_update(current, latest)`.
- `show_error(error)`.

## 2.6. Szelet F: support report

Statusz 2026-06-24 18:24 +02:00:

- Kesz: `core/support_report.py` URL-roviditessel, log tail olvasassal, support report epitesessel es `mailto:` link generálassal.
- Kesz: `utils/logging_setup.py`.
- Kesz: `core/self_check.py` es `app.py --self-check` parancs.
- Kesz: `tests/core/test_support_report.py` es `tests/core/test_self_check.py`.
- Validacio: `.venv-build\Scripts\python.exe -m pytest` -> `49 passed`.
- Megjegyzes: valos dev self-checkben `yt-dlp` es `ffmpeg` vendor hianyzik, ez build/vendor follow-up.

### `src/tecsoo_letolto/core/support_report.py`

```python
@dataclass(frozen=True)
class SupportContext:
    app_version: str
    windows_version: str
    ytdlp_version: str | None
    ffmpeg_version: str | None
    last_error_category: str | None
    last_error_summary: str | None
    output_dir_writable: bool | None
    mode: str | None
    timestamp: datetime
    url: str | None

def sanitize_url_for_report(url: str | None) -> str | None: ...
def tail_log_lines(log_path: Path, max_lines: int = 60) -> list[str]: ...
def build_support_report(context: SupportContext, log_lines: list[str]) -> str: ...
def open_mailto(report: str) -> None: ...
```

Support szabaly:

- SMTP nincs.
- `mailto:` nyilik alap levelezovel.
- Címzett: `attys@e-sper.hu`.
- Tárgy: `TecsoLetolto hibajelentés`.
- Előnézet kötelező.
- URL alapbol redaktalva: domain + opcionális video id, teljes query nelkul.

Teszt:

- URL redaction;
- log tail limit;
- report nem tartalmaz `token`, `cookie`, `password` mintat, ha inputban volt.

## 2.7. Szelet G: yt-dlp frissites

Statusz 2026-06-24 18:30 +02:00:

- Kesz: `services/update_service.py`.
- Kesz: csak `yt-dlp.exe` target cserelheto; mas EXE celpontot a service elutasit.
- Kesz: backup fajl neve `yt-dlp.previous.exe`; rollback tesztelve.
- Kesz: `tests/services/test_update_service.py`.
- Validacio: `.venv-build\Scripts\python.exe -m pytest` -> `65 passed`.
- Kesz: GUI gomb es felhasznaloi jovahagyasi dialog bekotese.

### `src/tecsoo_letolto/services/update_service.py`

```python
def get_current_ytdlp_version(tool: YtDlpTool) -> str: ...
def get_latest_ytdlp_version() -> str: ...
def download_ytdlp_release(temp_dir: Path) -> Path: ...
def verify_downloaded_ytdlp(exe: Path) -> str: ...
def replace_with_backup(current: Path, new_file: Path) -> None: ...
def rollback(previous: Path, current: Path) -> None: ...
```

Biztonsagi minimum:

1. Hivatalos yt-dlp release URL csak explicit allowlistbol.
2. Letoltes utan `yt-dlp.exe --version`.
3. Regi fajl: `yt-dlp.previous.exe`.
4. Ha uj nem fut, rollback.
5. Log minden lepesrol.
6. Felhasznaloi megerosites nelkul nincs update.

Megjegyzes:

- Frissitett dontes 2026-06-24: a GitHub release `SHA2-256SUMS` fajlja alapjan SHA-256 ellenorzes legyen, ha elerheto.

## 2.8. Szelet H: logging

### `src/tecsoo_letolto/utils/logging_setup.py`

```python
def configure_logging(log_dir: Path) -> Path: ...
def get_logger(name: str) -> logging.Logger: ...
```

Szabaly:

- Napi log: `tecsoletolto_YYYY-MM-DD.log`.
- UTF-8.
- Ne logoljon teljes env listat.
- URL-ek es pathok support reportban redaktalhatok, fejlesztoi logban csak indokoltan.

### `src/tecsoo_letolto/utils/redaction.py`

```python
SECRET_PATTERNS = ...
def redact_text(value: str) -> str: ...
def redact_path(value: str) -> str: ...
```

Teszt:

- `password=abc` -> `password=<redacted>`;
- `Bearer abc` -> `Bearer <redacted>`;
- `C:\Users\Name\Downloads` -> support reportban `...\Downloads`.

# 3. Build es release pipeline

Statusz 2026-06-24 18:33 +02:00:

- Reszben kesz: `scripts/build_dev.bat` letrehozza/hasznalja a `.venv-build` kornyezetet, telepiti a test extrat, futtatja a teszteket es a version smoke-ot.
- Reszben kesz: `scripts/build_release.bat` mar hivja a hivatalos yt-dlp fetch/verify scriptet, majd FFmpeg vendor preflightot futtat; teljes PyInstaller/release packaging meg nincs kesz.
- Reszben kesz: `scripts/verify_release.bat` ellenorzi a tervezett release mappa kotelezo es tiltott elemeit, de release payload meg nincs.
- Validacio: `scripts\build_dev.bat` -> zold, `65 passed`.
- Nyitott: PyInstaller build es teljes release ZIP artifact.

## 3.1. `scripts/build_release.bat`

Lepesek:

1. `py -3.12 -m venv .venv-build`
2. `.venv-build\Scripts\python.exe -m pip install --upgrade pip`
3. `.venv-build\Scripts\pip.exe install -e .[test]`
4. `.venv-build\Scripts\pytest.exe`
5. Release build dependency telepites csak build lepeshez: `.venv-build\Scripts\pip.exe install -e .[build]`
6. PyInstaller build:
   - entry: `src/tecsoo_letolto/app.py` vagy `-m tecsoo_letolto`;
   - name: `TecsoLetolto`;
   - icon: `src/tecsoo_letolto/resources/app.ico`;
   - one-folder elso korben.
7. `release/TecsoLetolto/` clean.
8. EXE bemasolas.
9. `scripts/fetch_ytdlp_vendor.bat` futtatasa, majd `vendor/yt-dlp/yt-dlp.exe` bemasolas.
10. `scripts/fetch_ffmpeg_vendor.bat` futtatasa, majd csak `vendor/ffmpeg/bin/ffmpeg.exe` es `vendor/ffmpeg/bin/ffprobe.exe` bemasolas.
11. `help/`, `licenses/`, `README_PORTABLE.txt`, `VERSION.txt` bemasolas.
12. `scripts/write_build_manifest.bat`.
13. `scripts/verify_release.bat`.
14. `artifacts/TecsoLetolto-<version>.zip`.

## 3.2. Build manifest

`artifacts/build_manifest.json` tartalom:

```json
{
  "appName": "TecsoLetolto",
  "version": "0.1.0-dev",
  "buildTime": "...",
  "gitCommit": "...",
  "pythonVersion": "...",
  "ytDlpVersion": "...",
  "ytDlpSha256": "...",
  "ytDlpSourceUrl": "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe",
  "ffmpegAssetName": "ffmpeg-master-latest-win64-lgpl.zip",
  "ffmpegSourceUrl": "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-lgpl.zip",
  "ffmpegVersion": "...",
  "ffmpegSha256": "...",
  "ffprobeVersion": "...",
  "ffprobeSha256": "...",
  "files": [
    {
      "path": "TecsoLetolto.exe",
      "size": 123,
      "sha256": "..."
    }
  ]
}
```

## 3.3. `scripts/verify_release.bat`

Ellenorzesek:

1. `release/TecsoLetolto/TecsoLetolto.exe` letezik.
2. `release/TecsoLetolto/vendor/yt-dlp/yt-dlp.exe` letezik.
3. `release/TecsoLetolto/vendor/ffmpeg/bin/ffmpeg.exe` letezik.
4. `release/TecsoLetolto/vendor/ffmpeg/bin/ffprobe.exe` letezik.
5. Nincs `release/TecsoLetolto/.venv`.
6. Nincs `release/TecsoLetolto/tests`.
7. Nincs `release/TecsoLetolto/__pycache__`.
8. Nincs `release/TecsoLetolto/*.py`, kiveve ha PyInstaller one-folder indokoltan tartalmaz ilyet; ezt kulon dokumentalni kell.
9. Nincs user media: `*.mp3`, `*.mkv`, `*.mp4` a release root alatt, kiveve dokumentalt sample nincs.
10. EXE indithato `--version` vagy `--self-check` modban.

# 4. Dokumentacio

Statusz 2026-06-24 18:33 +02:00:

- Reszben kesz: `README.md` felhasznaloi elso iranyba frissult.
- Reszben kesz: `docs/USER_GUIDE.md`, `docs/SUPPORT.md`, `docs/BUILD.md`, `docs/RELEASE.md`, `docs/RELEASE_TEST_CHECKLIST.md`, `docs/THIRD_PARTY_LICENSES.md`, `docs/CHANGELOG.md`.
- Nyitott: vegleges kepernyokep, pontos third-party license ellenorzes es release-specifikus reszletek.

## 4.1. README

Felhasznaloi elso:

1. Mi ez?
2. Mire hasznalhato jogszeruen?
3. Mire nem valo?
4. Gyors inditas portable csomagbol.
5. Link beillesztese.
6. Csak hang.
7. Video + hang.
8. Mentési mappa es fajlnev.
9. Frissites ellenorzese.
10. Support.
11. Fejlesztoi build csak kesobb.

## 4.2. `docs/USER_GUIDE.md`

Offline sugo forrasa:

- magyar;
- kepernyokep placeholder megengedett `TODO_SCREENSHOT`;
- legyen rovid jogszeru hasznalati figyelmeztetes.

## 4.3. `docs/SUPPORT.md`

- Hogyan keszul a hibajelentes.
- Mit tartalmaz.
- Mit nem tartalmaz.
- Hogyan ellenorizze a felhasznalo kuldes elott.

## 4.4. `docs/BUILD.md`

- Python 3.12.
- build dependency.
- vendor komponensek beszerzese.
- PyInstaller.
- release ellenorzes.

## 4.5. `docs/RELEASE.md`

- verzio bump;
- tesztek;
- build;
- manifest;
- ZIP;
- GitHub release;
- repo tisztasag.

## 4.6. `docs/RELEASE_TEST_CHECKLIST.md`

Az `ujratervezés.md` 19.2 pontjat kell atemelni checkbox listava.

## 4.7. `docs/THIRD_PARTY_LICENSES.md`

Minimum:

- yt-dlp;
- FFmpeg;
- Python;
- PyInstaller;
- tkinter/Tcl/Tk relevans licencinformacio, ha csomagolas erinti.

# 5. Tesztterv

## 5.1. Unit tesztek

Kotelezo elso kor:

1. `tests/core/test_filename_policy.py`
2. `tests/core/test_error_mapping.py`
3. `tests/core/test_paths.py`
4. `tests/core/test_support_report.py`
5. `tests/services/test_ytdlp_args.py`
6. `tests/services/test_ffmpeg_service.py`
7. `tests/utils/test_redaction.py`

## 5.2. Integration smoke

Kesziteni:

- `scripts/verify_release.bat`
- opcionális `python -m tecsoo_letolto --self-check`

Self-check:

1. app version kiirasa;
2. vendor yt-dlp check;
3. vendor ffmpeg check;
4. logs dir irhatosag;
5. Downloads dir irhatosag;
6. exit code `0`, ha minden rendben.

## 5.3. Kezi GUI smoke

Dokumentalando `docs/RELEASE_TEST_CHECKLIST.md` szerint:

- indulas tiszta Windows 10/11 alatt;
- nincs Python telepites;
- nincs kulso FFmpeg;
- nincs kulso yt-dlp;
- hibas URL magyar hiba;
- cancel mukodik;
- support preview mukodik;
- mappa megnyitas mukodik.

# 6. Regi fajlok sorsa

## 6.1. Megtartando atmenetileg

- Nincs mar megtartott regi futtatasi utvonal. A korabbi referencia fajlok torolve lettek, miutan az uj release self-check zold lett.

## 6.2. Atalakitas utan torlendo vagy archivalando

- Torolve: `letolto.py`, `letolto_gui.py`, `run.bat`, `run_gui.bat`, `run_gui_debug.bat`, `build_exe.bat`, `build_portable_installer.bat`, `requirements.txt`, `installer/`, `downloads/`, regi `.venv`, PyInstaller koztes `build/`, `dist/`, `TecsoLetolto.spec`.
- Ignored build/runtime output maradhat lokalis validaciohoz: `release/`, `artifacts/`, `vendor/`, `.venv-build/`.

## 6.3. Takaritasi riport

Keszitendo:

- `docs/codex-tasks/repo_cleanup_report.md`

Tartalom:

1. torolt fajlok;
2. megtartott fajlok;
3. athelyezett fajlok;
4. indoklas;
5. ismert kockazatok.

# 7. Biztonsagi es jogi kapuk

## 7.1. Tiltott funkciok

Nem keszulhet:

- DRM megkerules;
- login/cookie import;
- browser cookie olvasas;
- elofizeteses tartalom megkerules;
- regio bypass;
- SMTP jelszo vagy beepitett support account.

## 7.2. Secret/path audit

Release elott futtatando keresesi mintak:

```text
password
passwd
secret
token
apikey
api_key
smtp
FFMPEG_DIR
E:\
C:\Users
192.168.
10.
172.16.
```

Konkret jelenlegi allapot:

- A regi `letolto.py` torolve lett, igy a benne levo gepfuggo FFmpeg pelda sem maradt runtime utvonal.
- Az uj runtime vendor FFmpeg-et hasznal, lokalis `E:\...` vagy `C:\Users\...` FFmpeg fallback nelkul.

# 8. Elfogadasi matrix

Az implementacio akkor zart:

1. `pytest` zold.
2. `scripts/verify_release.bat` zold.
3. `TecsoLetolto.exe --self-check` zold.
4. `release/TecsoLetolto/` csak runtime payloadot tartalmaz.
5. `docs/USER_GUIDE.md`, `docs/SUPPORT.md`, `docs/BUILD.md`, `docs/RELEASE.md`, `docs/RELEASE_TEST_CHECKLIST.md`, `docs/THIRD_PARTY_LICENSES.md` kesz.
6. `README.md` felhasznaloi elso.
7. `STATE.md` aktualis.
8. `docs/CHANGELOG.dev.md` tartalmazza a fejlesztesi lepest.
9. `docs/codex-tasks/repo_cleanup_report.md` kesz.
10. Nincs gepfuggo hard-code.
11. Nincs secret/token/password.
12. Nincs user media vagy log commitra keszen.
13. A regi monolit inditasi logika vagy torolve, vagy kompatibilitasi okbol dokumentalt.

# 9. Javasolt commit-szeletek

1. `docs: add plug-and-play redesign plan`
   - ez a terv;
   - `STATE.md`;
   - `docs/CHANGELOG.dev.md`.
2. `chore: scaffold package and tests`
   - `src/tecsoo_letolto`;
   - `tests`;
   - `pyproject.toml`.
3. `feat: extract path and filename policies`
   - `core/paths.py`;
   - `core/filename_policy.py`;
   - unit tests.
4. `feat: add runtime tool services`
   - `ffmpeg_service.py`;
   - `ytdlp_service.py`;
   - subprocess runner;
   - tests.
5. `feat: add download manager and error mapping`
   - `download_manager.py`;
   - errors;
   - progress.
6. `feat: rebuild gui around service layer`
   - `gui/main_window.py`;
   - dialogs;
   - support preview.
7. `feat: add update and support workflows`
   - `update_service.py`;
   - `support_report.py`;
   - mailto preview.
8. `build: add release pipeline`
   - scripts;
   - manifest;
   - verify release.
9. `docs: refresh user and release documentation`
   - README;
   - user guide;
   - build/release/support/license docs.
10. `chore: clean legacy files`
   - regi BAT/monolit/installer maradek rendezese;
   - cleanup report.

# 10. Elso kovetkezo implementacios lepes

A kovetkezo konkret lepes legyen:

1. `pyproject.toml` bevezetese.
2. `src/tecsoo_letolto/core/filename_policy.py` es tesztjeinek megirasa.
3. `src/tecsoo_letolto/core/paths.py` es tesztjeinek megirasa.
4. `STATE.md` es `docs/CHANGELOG.dev.md` frissitese.

Ez kis kockazatu, mert nem bontja meg azonnal a mukodo regi letoltest, de megalapozza a teljes uj struktura legkritikusabb reszeit: mentési hely es biztonsagos fajlnev.
