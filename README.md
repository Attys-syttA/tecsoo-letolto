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

Parancsikon ikonhoz: a `assets/tecsoo-letolto.ico` fájlt tudod kiválasztani a parancsikon Tulajdonságok → Ikon módosítása résznél.

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

## EXE készítés (opcionális)

Ha szeretnéd “igazi” alkalmazásként futtatni (konzol nélkül), készíthetsz egy `.exe`-t PyInstallerrel:

```bat
build_exe.bat
```

Kimenet: `artifacts/TecsoLetolto.exe`

Megjegyzés: az így készült `.exe`-t a SmartScreen/Defender néha figyelmeztetésként jelölheti (különösen ha nincs aláírva) — ez gyakori saját build-eknél.

## “Telepítős” csomag (portable installer)

Készít egy olyan egyfájlos telepítőt, ami indításkor felkínálja a célmappa kiválasztását, majd kicsomagolja az alkalmazást **és a szükséges `ffmpeg`/`ffprobe` fájlokat**:

```bat
build_portable_installer.bat
```

Kimenet: `artifacts/TecsoLetolto-Installer.exe`
