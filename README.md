# TecsoLetolto

Magyar nyelvu, portable Windows alkalmazas jogszeruen mentheto online video- es hangtartalmak letoltesere.

## Fontos jogi figyelmeztetes

A program csak olyan tartalom mentesere hasznalhato, amelyhez a felhasznalonak joga van. Nem hasznalhato DRM megkerulesere, elofizeteses vagy zart tartalmak megszerzesere, cookie vagy bejelentkezesi adat importalasara.

## Celallapot

A kesz release egy kulon portable mappaban indul:

```text
release\TecsoLetolto\TecsoLetolto.exe
```

A felhasznalonak nem kell kulon Python, pip, FFmpeg vagy yt-dlp telepites.

## Jelenlegi allapot

A repo P&P ujratervezes alatt all. Az uj kod a `src/tecsoo_letolto/` mappaban epul. A regi `letolto.py`, `letolto_gui.py`, BAT inditok, regi installer scriptek es regi `requirements.txt` torolve lettek, miutan az uj PyInstaller release self-check zold lett.

## Fejlesztoi gyors ellenorzes

```bat
py -3.12 -m venv .venv-build
.venv-build\Scripts\python.exe -m pip install -e .[test]
.venv-build\Scripts\python.exe -m pytest
.venv-build\Scripts\python.exe -m tecsoo_letolto --version
```

Release build:

```bat
scripts\build_release.bat
scripts\verify_release.bat
```

## Dokumentacio

- `docs\USER_GUIDE.md`
- `docs\SUPPORT.md`
- `docs\BUILD.md`
- `docs\RELEASE.md`
- `docs\RELEASE_TEST_CHECKLIST.md`
- `docs\THIRD_PARTY_LICENSES.md`
