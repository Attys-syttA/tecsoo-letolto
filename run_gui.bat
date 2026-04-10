@echo off
setlocal

set "PYTHONUTF8=1"

REM Optional: change if ffmpeg is elsewhere
set "FFMPEG_DIR=E:\ffmpeg-2026-04-09-git-d3d0b7a5ee-essentials_build\bin"

REM Detach GUI into its own process (closing this window won't kill it)
pushd "%~dp0"

REM Prefer pyw.exe (windowed launcher). Fallback to py.exe -w.
where pyw >nul 2>nul
if %ERRORLEVEL%==0 (
  start "" pyw -3 "%~dp0letolto_gui.py"
) else (
  start "" py -3 -w "%~dp0letolto_gui.py"
)

popd
endlocal & exit /b 0
