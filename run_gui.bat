@echo off
setlocal

chcp 65001 >nul
set "PYTHONUTF8=1"

REM Opcionális: állítsd át, ha máshol van az ffmpeg
set "FFMPEG_DIR=E:\ffmpeg-2026-04-09-git-d3d0b7a5ee-essentials_build\bin"

py -3 "%~dp0letolto_gui.py"
endlocal
