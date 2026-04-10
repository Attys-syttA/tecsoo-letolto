@echo off
setlocal

REM Builds a Windows .exe for the GUI using PyInstaller.
REM Output: artifacts\TecsoLetolto.exe
REM Cleans build artifacts (build/, dist/, *.spec) after success.

pushd "%~dp0"

if not exist ".venv\\Scripts\\python.exe" (
  py -3 -m venv .venv
)

".venv\\Scripts\\python.exe" -m pip install -U pip
".venv\\Scripts\\python.exe" -m pip install -r requirements.txt
".venv\\Scripts\\python.exe" -m pip install pyinstaller

".venv\\Scripts\\pyinstaller.exe" --noconfirm --clean --onefile --windowed ^
  --name "TecsoLetolto" ^
  --icon "assets\\tecsoo-letolto.ico" ^
  "letolto_gui.py"

if not exist "dist\\TecsoLetolto.exe" (
  echo Build failed: dist\\TecsoLetolto.exe not found.
  popd
  exit /b 1
)

if not exist "artifacts" mkdir "artifacts" >nul 2>nul
copy /y "dist\\TecsoLetolto.exe" "artifacts\\TecsoLetolto.exe" >nul

REM Cleanup (keep .venv for faster rebuilds)
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
del /q "*.spec" >nul 2>nul

echo.
echo Done: "%~dp0artifacts\\TecsoLetolto.exe"
popd
endlocal
