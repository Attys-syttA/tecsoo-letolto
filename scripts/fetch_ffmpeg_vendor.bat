@echo off
setlocal

cd /d "%~dp0\.."

powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\tools\fetch-ffmpeg-vendor.ps1"
exit /b %ERRORLEVEL%
