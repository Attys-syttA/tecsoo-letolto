@echo off
setlocal

set "PYTHONUTF8=1"

REM Optional: change if ffmpeg is elsewhere
set "FFMPEG_DIR=E:\ffmpeg-2026-04-09-git-d3d0b7a5ee-essentials_build\bin"

REM Run GUI without keeping the console window open
start "" /b py -3 -w "%~dp0letolto_gui.py"
endlocal & exit /b 0
