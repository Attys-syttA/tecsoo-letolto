@echo off
setlocal

cd /d "%~dp0\.."

if not exist ".venv-build\Scripts\python.exe" (
  py -3.12 -m venv .venv-build
  if errorlevel 1 exit /b 1
)

".venv-build\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 exit /b 1

".venv-build\Scripts\python.exe" -m pip install -e .[test]
if errorlevel 1 exit /b 1

".venv-build\Scripts\python.exe" -m pytest
if errorlevel 1 exit /b 1

".venv-build\Scripts\python.exe" -m tecsoo_letolto --version
if errorlevel 1 exit /b 1

echo Development checks passed.
exit /b 0
