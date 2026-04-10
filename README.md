# tecsoo-letolto

YouTube videó letöltő + hang (mp3/m4a/opus stb.) kinyerés `yt-dlp` + `ffmpeg` alapon.

## Telepítés

```bat
py -3 -m pip install -r requirements.txt
```

## Használat

### GUI

```bat
run_gui.bat
```

### Parancssor (CLI)

Interaktív (bekéri a linket):

```bat
run.bat
```

MP3 hang kinyerés:

```bat
run.bat --mode audio "https://www.youtube.com/watch?v=..."
```

Videó letöltés (összefűzés mp4-be):

```bat
run.bat --mode video --container mp4 "https://www.youtube.com/watch?v=..."
```

Kimenet alapból: `./downloads`

## FFmpeg

Az `ffmpeg` bin mappa alapértelmezetten:

`E:\ffmpeg-2026-04-09-git-d3d0b7a5ee-essentials_build\bin`

Ha máshol van, add meg:

```bat
run.bat --ffmpeg-dir "D:\ffmpeg\bin" --mode audio "..."
```

vagy állítsd be környezeti változóként: `FFMPEG_DIR`.

Megjegyzés: ha a Windows SmartScreen/Defender blokkolja az `ffmpeg.exe` futtatását, a konvertálás/összefűzés nem fog működni. Ilyenkor használj megbízható forrásból származó ffmpeg csomagot (pl. `winget`/`choco`), vagy ellenőrzés után oldd fel a blokkolást a fájl Tulajdonságainál.

### Mi az a winget / choco?

- `winget`: a Windows beépített csomagkezelője (Windows Package Manager). Programok telepítésére/frissítésére jó parancssorból.
- `choco` (Chocolatey): népszerű külső csomagkezelő Windowsra (előbb telepíteni kell).

Keresés (a pontos csomagnév eltérhet):

```bat
winget search ffmpeg
choco search ffmpeg
```
