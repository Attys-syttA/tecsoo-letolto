@echo off
setlocal

REM Builds a Windows .exe for the GUI using PyInstaller.
REM Output: dist\TecsoLetolto.exe

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

echo.
echo Done: "%~dp0dist\\TecsoLetolto.exe"
popd
endlocal
