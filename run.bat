@echo off
setlocal

set "PYTHONUTF8=1"

REM Optional: change if ffmpeg is elsewhere
set "FFMPEG_DIR=E:\ffmpeg-2026-04-09-git-d3d0b7a5ee-essentials_build\bin"

REM If no args, the program will ask for the link
py -3 "%~dp0letolto.py" %*
set EXITCODE=%ERRORLEVEL%

if not "%EXITCODE%"=="0" (
  echo.
  echo Hiba (exit code=%EXITCODE%).
)

endlocal & exit /b %EXITCODE%
