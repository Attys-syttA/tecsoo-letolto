@echo off
setlocal

cd /d "%~dp0\.."

powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\tools\write-build-manifest.ps1"
exit /b %ERRORLEVEL%
