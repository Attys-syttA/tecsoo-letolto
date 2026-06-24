# Release folyamat

## Release elotti kapuk

1. Tesztek futnak: `.venv-build\Scripts\python.exe -m pytest`.
2. `scripts\fetch_ytdlp_vendor.bat` letolti a hivatalos stable `yt-dlp.exe` fajlt.
3. `vendor\yt-dlp\yt-dlp.exe --version` fut, es a verzio bekerul a build manifestbe.
4. A `yt-dlp.exe` SHA-256 ellenorzese sikeres a GitHub release `SHA2-256SUMS` fajlja alapjan.
5. `scripts\fetch_ffmpeg_vendor.bat` letolti a BtbN `ffmpeg-master-latest-win64-lgpl.zip` assetet.
6. `vendor\ffmpeg\bin\ffmpeg.exe -version` es `vendor\ffmpeg\bin\ffprobe.exe -version` fut.
7. FFmpeg/FFprobe verziok, SHA-256 hash-ek es source URL bekerulnek a build manifestbe.
8. Version smoke fut: `.venv-build\Scripts\python.exe -m tecsoo_letolto --version`.
9. Self-check fut a release mappabol.
10. `scripts\verify_release.bat` zold.
11. `docs\RELEASE_TEST_CHECKLIST.md` kezzel kitoltve.
12. Nincs secret vagy gepfuggo hard-code.
13. `STATE.md` es `docs\CHANGELOG.dev.md` friss.

## Artifactok

- `release\TecsoLetolto\`
- `artifacts\TecsoLetolto-<version>.zip`
- `artifacts\build_manifest.json`

Az `artifacts\build_manifest.json` tartalmazza legalabb:

- `ytDlpVersion`;
- `ytDlpSha256`;
- `ytDlpSourceUrl`;
- `ffmpegAssetName`;
- `ffmpegSourceUrl`;
- `ffmpegVersion`;
- `ffmpegSha256`;
- `ffprobeVersion`;
- `ffprobeSha256`.

## Tiltott release tartalom

- `.venv`;
- `tests`;
- `__pycache__`;
- user media;
- lokalis log;
- fejlesztoi dokumentumhalmaz;
- `.git`.

## yt-dlp forrasszabaly

Release-be csak a hivatalos `yt-dlp/yt-dlp` stable latest GitHub release `yt-dlp.exe` fajlja kerulhet:

```text
https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe
```

Tilos pipbol telepitett, `PATH`-bol talalt, nightly/master vagy mas repositorybol letoltott `yt-dlp` binarist hasznalni.

## FFmpeg forrasszabaly

Release-be csak a BtbN/FFmpeg-Builds latest release `ffmpeg-master-latest-win64-lgpl.zip` assetbol kinyert ket fajl kerulhet:

```text
vendor/ffmpeg/bin/ffmpeg.exe
vendor/ffmpeg/bin/ffprobe.exe
```

Tilos GPL, GPL-shared, nonfree, full buildre automatikusan valtani, es tilos lokalis fejlesztoi FFmpeg utvonalra vagy rendszer `PATH`-ra epiteni. Ha az exact asset nev nem talalhato, a release folyamat megall es emberi dontest ker.
