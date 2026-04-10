@echo off
setlocal

REM Builds:
REM  - GUI app: artifacts\TecsoLetolto.exe
REM  - Self-extracting installer: artifacts\TecsoLetolto-Installer.exe
REM Cleans build artifacts (build/, dist/, installer/_payload, installer/payload.zip, *.spec) after success.
REM
REM The installer asks for a target folder and extracts:
REM   TecsoLetolto\TecsoLetolto.exe
REM   TecsoLetolto\ffmpeg\bin\ffmpeg.exe
REM   TecsoLetolto\ffmpeg\bin\ffprobe.exe

pushd "%~dp0"

if not exist ".venv\\Scripts\\python.exe" (
  py -3 -m venv .venv
)

".venv\\Scripts\\python.exe" -m pip install -U pip
".venv\\Scripts\\python.exe" -m pip install -r requirements.txt
".venv\\Scripts\\python.exe" -m pip install pyinstaller

REM 1) Build the GUI exe
call build_exe.bat
if not "%ERRORLEVEL%"=="0" (
  echo GUI build failed.
  popd
  exit /b 1
)

REM 2) Build payload.zip containing app + ffmpeg
".venv\\Scripts\\python.exe" "installer\\build_installer.py" --gui-exe "artifacts\\TecsoLetolto.exe" --out-zip "installer\\payload.zip"
if not "%ERRORLEVEL%"=="0" (
  echo Payload build failed.
  popd
  exit /b 1
)

REM 3) Build the installer exe (onefile, windowed)
".venv\\Scripts\\pyinstaller.exe" --noconfirm --clean --onefile --windowed ^
  --name "TecsoLetolto-Installer" ^
  --icon "assets\\tecsoo-letolto.ico" ^
  --add-data "installer\\payload.zip;." ^
  "installer\\installer_app.py"

if not exist "dist\\TecsoLetolto-Installer.exe" (
  echo Installer build failed: dist\\TecsoLetolto-Installer.exe not found.
  popd
  exit /b 1
)

if not exist "artifacts" mkdir "artifacts" >nul 2>nul
copy /y "dist\\TecsoLetolto-Installer.exe" "artifacts\\TecsoLetolto-Installer.exe" >nul

REM Cleanup (keep .venv for faster rebuilds)
if exist "installer\\_payload" rmdir /s /q "installer\\_payload"
if exist "installer\\payload.zip" del /q "installer\\payload.zip"
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
del /q "*.spec" >nul 2>nul

echo.
echo Done: "%~dp0artifacts\\TecsoLetolto-Installer.exe"
popd
endlocal
