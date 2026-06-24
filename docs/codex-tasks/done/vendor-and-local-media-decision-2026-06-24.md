# Status

- Allapot: done / vendor es helyi media dontesek rogzitve es atvezetve.
- Letrehozva: 2026-06-24.
- Kapcsolodo lezart terv: `docs/codex-tasks/done/tecsoletolto-plug-and-play-redesign-plan-2026-06-24.md`

# Döntés 1: vendor komponensek forrasa

A teljes P&P release-hez kell:

- `vendor/yt-dlp/yt-dlp.exe`
- `vendor/ffmpeg/bin/ffmpeg.exe`
- `vendor/ffmpeg/bin/ffprobe.exe`

## Reszben eldolt: `yt-dlp.exe`

- Dontes datum: 2026-06-24.
- A release-be kerulo `yt-dlp.exe` forrasa a hivatalos `yt-dlp/yt-dlp` GitHub stable latest release.
- Hasznalt fajl: Windows standalone x64 binary, `yt-dlp.exe`.
- Letoltesi URL: `https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe`.
- Ellenorzes:
  - letoltes utan futtatni kell: `vendor/yt-dlp/yt-dlp.exe --version`;
  - a verziot a build manifestbe be kell irni;
  - ha elerheto, a `SHA2-256SUMS` fajl alapjan SHA-256 ellenorzes kell.
- A letoltott binaris nem commitolhato a forrasrepoba.
- A binaris csak release payloadba kerulhet.
- Tilos:
  - pipbol telepitett `yt-dlp` runtime dependencykent;
  - rendszer `PATH` alapjan keresett `yt-dlp`;
  - nightly vagy master csatornara automatikusan valtani;
  - mas repositorybol `yt-dlp` binarist letolteni;
  - felhasznaloi jovahagyas nelkuli frissites.
- Az elso belso frissito csak ezt frissitheti: `vendor/yt-dlp/yt-dlp.exe`.

## Eldolt: FFmpeg / FFprobe

- Dontes datum: 2026-06-24.
- A release-be kerulo FFmpeg/FFprobe forrasa a `BtbN/FFmpeg-Builds` GitHub projekt.
- Valasztott build:
  - Windows x64;
  - LGPL variant;
  - static zip build, ha elerheto.
- Preferalt asset-nev: `ffmpeg-master-latest-win64-lgpl.zip`.
- Ha ez az asset-nev a GitHub release-ben valtozik vagy nem talalhato, Codex nem valaszthat onalloan GPL/full/nonfree buildet. Ilyenkor meg kell allni, dokumentalni kell a problemat, es emberi dontest kell kerni.
- A release payloadba csak ezek kerulhetnek:
  - `vendor/ffmpeg/bin/ffmpeg.exe`;
  - `vendor/ffmpeg/bin/ffprobe.exe`.
- Nem kell:
  - `ffplay.exe`;
  - dokumentacios HTML;
  - pelda media;
  - extra DLL, kiveve ha a valasztott build mukodesehez tenylegesen szukseges.
- Tilos:
  - GPL build;
  - GPL-shared build;
  - nonfree build;
  - full build, ha LGPL essentials/static alternativa eleg;
  - lokalis `E:\` vagy `C:\Users\...` fejlesztoi FFmpeg utvonal;
  - rendszer `PATH`-bol talalt FFmpeg mint release dependency.
- Ellenorzes:
  - `vendor/ffmpeg/bin/ffmpeg.exe -version`;
  - `vendor/ffmpeg/bin/ffprobe.exe -version`;
  - verziok rogzitese `artifacts/build_manifest.json` fajlban;
  - SHA-256 hash rogzitese `artifacts/build_manifest.json` fajlban;
  - forras URL rogzítese `docs/THIRD_PARTY_LICENSES.md` fajlban.

## Lezart kerdesek

1. A nem release payloadba szant vendor cache fajlok `vendor/` alatt, gitignored lokalis cache-kent maradhatnak, de nem commitolhatok a forrasrepoba.

## Javasolt alapdontes

- Forrasrepoba ne keruljon nagy binaris vendor payload.
- `yt-dlp.exe` build elott dokumentalt fetch scripttel keruljon `vendor/yt-dlp/` ala.
- FFmpeghez legyen dokumentalt fetch script, amely csak a preferalt BtbN LGPL win64 static zip assetet fogadja el.
- Release artifactba keruljenek be az ellenorzott vendor fajlok.

# Döntés 2: helyi `downloads/` mappa sorsa

A jelenlegi repo alatt van `downloads/` mappa, amely valos vagy tesztelesbol visszamaradt mediafajlokat tartalmazhat.

## Eldolt

- Dontes datum: 2026-06-24.
- A repo alatti `downloads/` mappaban levo teszt soran letoltott anyagok torolhetok.
- A mappa nem Git payload es nem release payload.
- Codex torolheti a mappat a repo-takaritas soran.

## Javasolt alapdontes

- Ne legyen Git payload.
- A mappa torolve lett a munkafabol 2026-06-24-en.

# Döntés 3: regi futtatasi utvonalak torlese

A regi fajlokban meg vannak gepfuggo FFmpeg utak:

- `letolto.py`
- `run.bat`
- `run_gui.bat`
- `run_gui_debug.bat`
- `installer/build_installer.py`

## Eldolt

- Dontes datum: 2026-06-24.
- A regi futtatasi utvonal torolheto, miutan az uj PyInstaller one-folder release `--version`, `--self-check` es `scripts\verify_release.bat` kapuja zold.
- A torles megtortent 2026-06-24-en.

## Javasolt alapdontes

- `letolto.py`, `letolto_gui.py`, regi BAT inditok, regi build BAT-ok, regi `installer/` scriptek es regi `requirements.txt` torolve.
