# Build

## Kovetelmenyek

- Windows 10/11 x64.
- Python 3.12.
- Git.
- A release buildhez kulon biztositott vagy letoltott vendor komponensek:
  - `yt-dlp.exe` hivatalos yt-dlp GitHub stable release-bol;
  - `ffmpeg.exe` a BtbN/FFmpeg-Builds `ffmpeg-master-latest-win64-lgpl.zip` assetbol;
  - `ffprobe.exe` ugyanabbol a BtbN LGPL win64 static zip assetbol.

## Fejlesztoi teszt

```bat
py -3.12 -m venv .venv-build
.venv-build\Scripts\python.exe -m pip install --upgrade pip
.venv-build\Scripts\python.exe -m pip install -e .[test]
.venv-build\Scripts\python.exe -m pytest
```

## Release build cel

A kesz portable mappa:

```text
release\TecsoLetolto\
```

Ebbe csak runtime payload kerulhet, fejlesztoi forras, teszt, cache vagy user media nem.

## Installer build

Ha a friss portable release-bol Windows telepitot is szeretnel kesziteni:

```bat
scripts\build_installer.bat
```

Ez ujraepiti es ellenorzi a `release\TecsoLetolto\` mappat, majd legyartja:

- `artifacts\TecsoLetolto-Installer.exe`
- `artifacts\TecsoLetolto-Installer-<version>.exe`

Az uj installer a mostani GUI payloadot csomagolja be, nem a regi aprilisi IExpress csomagot.

## yt-dlp vendor beszerzes

`yt-dlp.exe` nem runtime Python dependency es nem a rendszer `PATH`-bol jon. A build elott a hivatalos stable GitHub release-bol kell letolteni:

```text
https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe
```

Ellenorzes:

```bat
scripts\fetch_ytdlp_vendor.bat
vendor\yt-dlp\yt-dlp.exe --version
```

A script letolti a `SHA2-256SUMS` fajlt is, es csak sikeres SHA-256 ellenorzes utan hagyja meg a vendor peldanyt. A `vendor/` mappa gitignored; a binaris csak release payloadba kerulhet. A verzio es hash metaadatot a build manifestnek tartalmaznia kell.

## FFmpeg vendor beszerzes

FFmpeg es FFprobe nem a rendszer `PATH`-bol es nem lokalis fejlesztoi `E:\` vagy `C:\Users\...` utvonalrol jon. A build elott a BtbN/FFmpeg-Builds latest release pontosan ilyen assetjet kell hasznalni:

```text
ffmpeg-master-latest-win64-lgpl.zip
```

Ellenorzes:

```bat
scripts\fetch_ffmpeg_vendor.bat
vendor\ffmpeg\bin\ffmpeg.exe -version
vendor\ffmpeg\bin\ffprobe.exe -version
```

A script csak ezt az exact asset-nevet fogadja el. Ha nem talalja, megall, mert nem valaszthat automatikusan GPL/full/nonfree buildet. A release payloadba csak `vendor\ffmpeg\bin\ffmpeg.exe` es `vendor\ffmpeg\bin\ffprobe.exe` kerulhet. A verziok, SHA-256 hash-ek es source URL-ek a `scripts\write_build_manifest.bat` altal keszitett `artifacts\build_manifest.json` fajlba kerulnek.
