# Third-party licenses

Ez a fajl a release elott pontositando licenc-osszefoglalo helye.

## yt-dlp

- Projekt: yt-dlp
- Felhasznalas: kulso `yt-dlp.exe` komponens a letolteshez.
- Release forras: hivatalos `yt-dlp/yt-dlp` stable GitHub release, `https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe`.
- Licenc: release elott az aktualis upstream licenc szerint ellenorizendo.

## FFmpeg

- Projekt: FFmpeg
- Felhasznalas: audio kinyereshez es video/hang osszefuzeshez.
- Release forras: BtbN/FFmpeg-Builds latest release, preferalt asset `ffmpeg-master-latest-win64-lgpl.zip`.
- Source URL: `https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-lgpl.zip`.
- Valasztott varians: Windows x64 LGPL static zip build.
- Release payload: csak `vendor/ffmpeg/bin/ffmpeg.exe` es `vendor/ffmpeg/bin/ffprobe.exe`.
- Licenc: LGPL varians; release elott a konkret upstream licencfajlok alapjan vegsoen ellenorizendo.

## Python / PyInstaller

- Felhasznalas: alkalmazas runtime/build csomagolas.
- Licenc: release elott a hasznalt komponensek szerint ellenorizendo.
