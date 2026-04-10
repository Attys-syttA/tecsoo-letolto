@echo off
setlocal

set "PYTHONUTF8=1"

REM Optional: change if ffmpeg is elsewhere
set "FFMPEG_DIR=E:\ffmpeg-2026-04-09-git-d3d0b7a5ee-essentials_build\bin"

pushd "%~dp0"
py -3 "%~dp0letolto_gui.py"
set EXITCODE=%ERRORLEVEL%
popd

echo.
echo Exit code=%EXITCODE%
pause
endlocal & exit /b %EXITCODE%
