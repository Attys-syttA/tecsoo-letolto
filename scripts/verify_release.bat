@echo off
setlocal

cd /d "%~dp0\.."
set RELEASE_DIR=release\TecsoLetolto

if not exist "%RELEASE_DIR%\TecsoLetolto.exe" (
  echo Missing %RELEASE_DIR%\TecsoLetolto.exe
  exit /b 1
)

if not exist "%RELEASE_DIR%\vendor\yt-dlp\yt-dlp.exe" (
  echo Missing %RELEASE_DIR%\vendor\yt-dlp\yt-dlp.exe
  exit /b 1
)

if not exist "%RELEASE_DIR%\vendor\ffmpeg\bin\ffmpeg.exe" (
  echo Missing %RELEASE_DIR%\vendor\ffmpeg\bin\ffmpeg.exe
  exit /b 1
)

if not exist "%RELEASE_DIR%\vendor\ffmpeg\bin\ffprobe.exe" (
  echo Missing %RELEASE_DIR%\vendor\ffmpeg\bin\ffprobe.exe
  exit /b 1
)

if exist "%RELEASE_DIR%\.venv" (
  echo Forbidden release content: .venv
  exit /b 1
)

if exist "%RELEASE_DIR%\tests" (
  echo Forbidden release content: tests
  exit /b 1
)

if exist "%RELEASE_DIR%\__pycache__" (
  echo Forbidden release content: __pycache__
  exit /b 1
)

if exist "%RELEASE_DIR%\tests" (
  echo Forbidden release content: tests
  exit /b 1
)

"%RELEASE_DIR%\TecsoLetolto.exe" --version
if errorlevel 1 exit /b 1

"%RELEASE_DIR%\TecsoLetolto.exe" --self-check
if errorlevel 1 exit /b 1

echo Release folder verification passed.
exit /b 0
