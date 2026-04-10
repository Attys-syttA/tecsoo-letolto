@echo off
setlocal

REM Builds:
REM  - GUI app: dist\TecsoLetolto.exe
REM  - Self-extracting installer: installer_dist\TecsoLetolto-Installer.exe
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
".venv\\Scripts\\python.exe" "installer\\build_installer.py" --out-zip "installer\\payload.zip"
if not "%ERRORLEVEL%"=="0" (
  echo Payload build failed.
  popd
  exit /b 1
)

REM 3) Build the installer exe (onefile, windowed)
if exist "installer_dist" rmdir /s /q "installer_dist"

".venv\\Scripts\\pyinstaller.exe" --noconfirm --clean --onefile --windowed ^
  --name "TecsoLetolto-Installer" ^
  --icon "assets\\tecsoo-letolto.ico" ^
  --add-data "installer\\payload.zip;." ^
  "installer\\installer_app.py"

if exist "dist\\TecsoLetolto-Installer.exe" (
  mkdir installer_dist >nul 2>nul
  move /y "dist\\TecsoLetolto-Installer.exe" "installer_dist\\TecsoLetolto-Installer.exe" >nul
)

echo.
echo Done: "%~dp0installer_dist\\TecsoLetolto-Installer.exe"
popd
endlocal
