@echo off
setlocal

cd /d "%~dp0\.."

for /d /r %%D in (__pycache__) do (
  if exist "%%D" rmdir /s /q "%%D"
)

for /d /r %%D in (*.egg-info) do (
  if exist "%%D" rmdir /s /q "%%D"
)

if exist ".pytest_cache" rmdir /s /q ".pytest_cache"
if exist ".serena" rmdir /s /q ".serena"
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "TecsoLetolto.spec" del /q "TecsoLetolto.spec"

del /s /q *.pyc 1>nul 2>nul
del /s /q *.pyo 1>nul 2>nul

echo Removed local cache and intermediate build files.
exit /b 0
