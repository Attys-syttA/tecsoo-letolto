# Codex-agent feladat: `tecsoo-letolto` teljes újratervezése és tiszta plug-and-play Windows alkalmazássá alakítása

## 0. Alapfeladat

A `https://github.com/Attys-syttA/tecsoo-letolto` repóban lévő jelenlegi programot teljesen újra kell tervezni és termékszerű állapotba kell hozni.

A cél nem egyszerű javítás és nem felületi ráncfelvarrás, hanem egy olyan, laikus felhasználó számára is használható, hordozható Windows alkalmazás elkészítése, amelyhez a felhasználónak nem kell Python-t, pip-et, FFmpeg-et, yt-dlp-t vagy parancssori eszközt külön telepítenie.

A végállapot: egy tiszta repó, áttekinthető forráskóddal, dokumentációval, tesztekkel, build-folyamattal és egy külön mappába előállított kész programmal.

---

## 1. Munkamódszer

### 1.1. Szigorú sorrend

A fejlesztést az alábbi sorrendben kell végezni:

1. Repo audit.
2. Jelenlegi működés feltérképezése.
3. Új célarchitektúra megtervezése.
4. Implementációs terv készítése.
5. Implementáció.
6. Tesztelés.
7. Build / release csomag előállítása.
8. Régi, felesleges maradékok törlése.
9. Repo-tisztítás.
10. Végső ellenőrzés és állapotjelentés.

Nem szabad vakon átírni a repót. Előbb meg kell érteni, mi van benne, mi használható újra, mi elavult, és mi törlendő.

### 1.2. Változtatási szabály

Minden jelentős módosítás előtt legyen rövid terv, majd a módosítás után legyen ellenőrzés.

A fejlesztés során kerülni kell a nagy, áttekinthetetlen módosításokat. A munka legyen szakaszolva:

* audit commit,
* struktúra rendezés,
* core logika,
* GUI,
* support / diagnosztika,
* build / installer,
* dokumentáció,
* takarítás.

### 1.3. Biztonsági szabály

Semmilyen titkos adat nem kerülhet a repóba:

* SMTP jelszó,
* API kulcs,
* token,
* személyes jelszó,
* privát útvonal,
* fix gépnév,
* fix belső IP,
* fix `E:\...` vagy más helyi fejlesztői útvonal.

Ha bármilyen ilyen adat szerepel a jelenlegi repóban, azt el kell távolítani.

---

## 2. Célplatform

A célplatform:

* Windows 10 x64,
* Windows 11 x64.

A programnak lehetőleg ne igényeljen rendszergazdai jogosultságot.

A programnak ne legyen szüksége:

* külön Python telepítésre,
* külön pip telepítésre,
* külön FFmpeg telepítésre,
* külön yt-dlp telepítésre,
* külön parancssori használatra.

---

## 3. Repo-szerkezet

A repót át kell rendezni tiszta, fenntartható szerkezetre.

Javasolt végső struktúra:

```text
tecsoo-letolto/
│
├─ src/
│  └─ tecsoo_letolto/
│     ├─ __init__.py
│     ├─ app.py
│     ├─ gui/
│     ├─ core/
│     ├─ services/
│     ├─ utils/
│     └─ resources/
│
├─ tests/
│
├─ docs/
│  ├─ USER_GUIDE.md
│  ├─ SUPPORT.md
│  ├─ BUILD.md
│  ├─ RELEASE.md
│  ├─ THIRD_PARTY_LICENSES.md
│  ├─ CHANGELOG.md
│  └─ codex-tasks/
│
├─ scripts/
│  ├─ build_dev.bat
│  ├─ build_release.bat
│  ├─ clean_repo.bat
│  └─ verify_release.bat
│
├─ release/
│  └─ TecsoLetolto/
│
├─ artifacts/
│
├─ AGENTS.md
├─ STATE.md
├─ README.md
├─ pyproject.toml
├─ .gitignore
└─ LICENSE
```

### 3.1. Fontos szabály

A `release/TecsoLetolto/` mappába kizárólag a kész futtatható program kerülhet.

Nem kerülhet oda:

* forráskód,
* `.venv`,
* `__pycache__`,
* build cache,
* tesztfájl,
* ideiglenes ZIP,
* fejlesztői napló,
* régi programmaradék,
* letöltött felhasználói média.

Az `artifacts/` mappába kerülhet:

* ZIP csomag,
* telepítő,
* build manifest,
* release notes.

---

## 4. Alkalmazás neve és célja

A program neve legyen egységesen:

```text
TecsoLetolto
```

A program célja:

* felhasználó által megadott, jogszerűen menthető online videó/hang tartalom letöltése;
* hangfájl kinyerése;
* videó + hang együttes mentése;
* egyszerű, magyar nyelvű, laikusoknak is érthető GUI biztosítása.

A program ne állítsa magáról, hogy hivatalos YouTube alkalmazás.

A programban és a dokumentációban szerepeljen rövid jogszerű használati figyelmeztetés:

```text
A program csak olyan tartalom mentésére használható, amelyhez a felhasználónak joga van. Ilyen lehet például saját tartalom, engedéllyel letölthető tartalom, közkincs vagy oktatási/teszt célú tartalom. A program nem használható jogosulatlan hozzáférésre, DRM megkerülésére vagy előfizetéses/zárt tartalmak megszerzésére.
```

---

## 5. Tiltott funkciók

A program nem tartalmazhat:

* DRM megkerülést,
* bejelentkezési adatok bekérését,
* YouTube cookie importot,
* böngésző cookie olvasást,
* előfizetéses vagy zárt tartalom megkerülését,
* regionális korlátozás vagy hozzáférési korlát megkerülését,
* jelszavak, tokenek vagy munkamenetek kezelését.

---

## 6. Fő funkciók

### 6.1. GUI mezők

A főablakon legyenek az alábbi elemek:

1. Link mező

   * ide illeszthető be a cél URL;
   * legyen nagy, jól olvasható mező;
   * legyen mellette “Beillesztés” gomb.

2. Mentési mappa mező

   * legyen kézzel szerkeszthető;
   * legyen mellette “Tallózás” gomb;
   * ha üres, a Windows felhasználói Letöltések mappáját használja.

3. Fájlnév mező

   * opcionális;
   * ha üres, a program automatikusan generáljon biztonságos fájlnevet;
   * a generált fájlnév tartalmazza a média címét és dátumot.

4. Letöltési mód választó

   * “Csak hang”;
   * “Videó + hang”.

5. Hangformátum választó

   * alapértelmezett: `mp3`;
   * választható: `mp3`, `m4a`, `opus`, esetleg `wav`;
   * a túl sok technikai opciót kerülni kell.

6. Videóformátum választó

   * alapértelmezett: `mp4`;
   * opcionálisan: `mkv`;
   * laikus módon magyarázva.

7. Minőség választó

   * egyszerű választó:

     * “Normál”,
     * “Jó”,
     * “Legjobb elérhető”.
   * ne nyers technikai paramétert kelljen beírni.

8. Letöltés indítása gomb.

9. Letöltés megszakítása gomb.

10. Mezők törlése gomb.

11. Mappa megnyitása gomb.

12. Tálcára minimalizálás gomb.

13. Súgó gomb.

14. Support gomb.

15. Névjegy / verzió gomb.

16. Kilépés gomb.

---

## 7. GUI elvárások

A GUI legyen:

* egyszerű,
* magyar nyelvű,
* jól olvasható,
* nem zsúfolt,
* kezdők számára is érthető,
* legalább 10–11 pontos betűmérettel,
* megfelelő térközökkel,
* átméretezhető ablakkal.

Kerülendő:

* túl kicsi feliratok,
* túl sok technikai opció,
* nyers log ömlesztése a felhasználó elé,
* parancssori jellegű hibaüzenetek.

A főablakban legyen rövid státuszsor:

```text
Készen áll.
Letöltés előkészítése...
Letöltés folyamatban...
Hang kinyerése...
Videó összefűzése...
Kész.
Hiba történt.
```

Legyen vizuális folyamatjelző, ha a backend ezt lehetővé teszi.

---

## 8. Alapértelmezett mentési logika

Ha a felhasználó nem ad meg mentési mappát, akkor a program a Windows felhasználói Letöltések mappájába mentsen.

Példa:

```text
C:\Users\<felhasználó>\Downloads
```

Ne a program saját mappájába mentsen alapértelmezetten.

Ha a célmappa nem létezik:

* a program próbálja létrehozni;
* ha nem sikerül, adjon érthető magyar hibaüzenetet.

---

## 9. Fájlnévkezelés

### 9.1. Automatikus fájlnév

Ha a felhasználó nem ad meg fájlnevet, akkor a program a média metaadataiból készítsen fájlnevet.

Javasolt séma:

```text
<cím>_<YYYY-MM-DD>.<kiterjesztés>
```

Ha cím nem nyerhető ki:

```text
letoltes_<YYYY-MM-DD>_<HHMMSS>.<kiterjesztés>
```

### 9.2. Biztonságos fájlnév

A fájlnévből el kell távolítani vagy cserélni kell a Windows alatt tiltott karaktereket:

```text
< > : " / \ | ? *
```

Tilos legyen üres, ponttal végződő vagy Windows által fenntartott név.

Például:

```text
CON
PRN
AUX
NUL
COM1
LPT1
```

### 9.3. Fájlnév-ütközés

Ha már létezik azonos nevű fájl, a program ne írja felül automatikusan.

Követendő működés:

1. alapértelmezés szerint automatikusan fűzzön sorszámot:

   * `_01`,
   * `_02`,
   * `_03`.

2. opcionálisan kérdezzen rá:

   * felülírás,
   * új név generálása,
   * megszakítás.

A biztonságos alapértelmezés: ne írjon felül.

---

## 10. Letöltőmotor

### 10.1. Backend absztrakció

A letöltési logika ne legyen közvetlenül a GUI-ba égetve.

Legyen külön réteg:

```text
core/download_manager.py
core/media_info.py
core/filename_policy.py
core/error_mapping.py
services/ytdlp_service.py
services/ffmpeg_service.py
```

A GUI csak a szolgáltatásréteget hívja.

### 10.2. yt-dlp használat

A program használhatja a `yt-dlp` projektet, de ne függjön a felhasználó gépén telepített példánytól.

A plug-and-play cél miatt javasolt architektúra:

```text
release/TecsoLetolto/
├─ TecsoLetolto.exe
├─ vendor/
│  ├─ yt-dlp/
│  │  └─ yt-dlp.exe
│  └─ ffmpeg/
│     └─ bin/
│        ├─ ffmpeg.exe
│        └─ ffprobe.exe
```

A GUI alkalmazás a saját `vendor/yt-dlp/yt-dlp.exe` példányát hívja meg.

Ez azért javasolt, mert így a `yt-dlp` frissíthető anélkül, hogy az egész programot újra kellene építeni.

### 10.3. FFmpeg használat

Az FFmpeg ne külső telepítésből legyen elvárva.

A kész program tartalmazza:

```text
ffmpeg.exe
ffprobe.exe
```

A program először a saját csomagolt FFmpeg példányát keresse.

Tilos beégetett fejlesztői útvonalat használni.

Tilos ilyen útvonal:

```text
E:\ffmpeg...
D:\...
C:\Users\Attila...
```

### 10.4. Ellenőrzés indításkor

A program induláskor vagy első letöltés előtt ellenőrizze:

* létezik-e `yt-dlp.exe`,
* futtatható-e `yt-dlp.exe --version`,
* létezik-e `ffmpeg.exe`,
* futtatható-e `ffmpeg.exe -version`,
* létezik-e `ffprobe.exe`,
* írható-e a célmappa.

Ha valamelyik hiányzik, adjon rövid, érthető magyar hibát.

---

## 11. yt-dlp belső frissítése

### 11.1. Frissítés ellenőrzése

Legyen “Frissítés ellenőrzése” funkció.

Ez ellenőrizze:

* jelenlegi beépített yt-dlp verzió,
* elérhető új yt-dlp verzió,
* van-e újabb stabil kiadás.

A felhasználónak világosan jelenjen meg:

```text
Jelenlegi yt-dlp verzió: ...
Elérhető verzió: ...
Szeretnéd frissíteni?
```

### 11.2. Frissítés menete

A frissítés ne történjen automatikusan és ne történjen vakon.

Követendő folyamat:

1. verzió lekérdezése;
2. felhasználói megerősítés;
3. új `yt-dlp.exe` letöltése hivatalos forrásból;
4. régi `yt-dlp.exe` biztonsági mentése;
5. új fájl ellenőrzése;
6. próbaindítás `yt-dlp.exe --version`;
7. siker esetén új verzió aktiválása;
8. hiba esetén visszaállás a régi verzióra.

### 11.3. Rollback

Ha frissítés után a `yt-dlp.exe` nem fut, a program állítsa vissza az előző működő példányt.

Legyen például:

```text
vendor/yt-dlp/yt-dlp.exe
vendor/yt-dlp/yt-dlp.previous.exe
```

### 11.4. Naplózás

A frissítés minden lépése kerüljön naplóba.

A felhasználó számára csak rövid üzenet jelenjen meg.

---

## 12. Hibaüzenetek és diagnosztika

### 12.1. Hibaosztályok

A program ne nyers Python tracebacket mutasson a felhasználónak.

A hibákat kategorizálja:

1. Hibás vagy üres link.
2. Nem támogatott link.
3. Nincs internetkapcsolat.
4. A tartalom nem érhető el.
5. A tartalom korlátozott.
6. A letöltés megszakadt.
7. Nincs jogosultság a célmappához.
8. Nincs elég tárhely.
9. FFmpeg hiba.
10. yt-dlp hiba.
11. Ismeretlen hiba.

### 12.2. Felhasználói hibaüzenet

A felhasználó ilyen jellegű üzenetet kapjon:

```text
Nem sikerült letölteni a megadott tartalmat.

Valószínű ok:
A link nem érhető el, vagy a tartalom korlátozott.

Mit próbálhatsz meg:
- Ellenőrizd, hogy a link böngészőben megnyitható-e.
- Ellenőrizd az internetkapcsolatot.
- Próbáld meg frissíteni a letöltő komponenst a “Frissítés ellenőrzése” gombbal.
```

### 12.3. Részletes technikai napló

A részletes hiba ne a főablakba ömöljön.

Legyen:

```text
%LOCALAPPDATA%\TecsoLetolto\logs\
```

A logfájl neve például:

```text
tecsoletolto_YYYY-MM-DD.log
```

A log ne tartalmazzon:

* jelszót,
* tokent,
* cookie-t,
* személyes levelezési adatot,
* teljes környezeti változó listát.

---

## 13. Support funkció

### 13.1. Support gomb célja

A Support gomb ne közvetlen SMTP-jelszóval küldjön e-mailt.

A program a felhasználó alapértelmezett levelezőprogramját nyissa meg előre kitöltött levéllel.

Címzett:

```text
attys@e-sper.hu
```

Tárgy:

```text
TecsoLetolto hibajelentés
```

### 13.2. Hibajelentés tartalma

A program készítsen elő egy rövid hibajelentést.

Tartalma:

* program neve,
* program verziója,
* Windows verzió,
* yt-dlp verzió,
* FFmpeg verzió,
* utolsó hiba kategóriája,
* utolsó hiba rövid leírása,
* utolsó 30–80 releváns naplósor,
* célmappa írhatóságának eredménye,
* letöltési mód,
* időpont.

Ne tartalmazzon:

* SMTP jelszót,
* tokent,
* cookie-t,
* teljes személyes útvonalat, ha nem szükséges,
* teljes URL-t, ha az érzékeny lehet.

A teljes URL helyett opcionálisan csak a domain és az azonosító szerepeljen, vagy a felhasználó dönthesse el, belekerüljön-e.

### 13.3. Felhasználói kontroll

Küldés előtt jelenjen meg előnézet:

```text
Az alábbi hibajelentést fogja megnyitni a levelezőprogramban.
Kérlek, ellenőrizd, hogy nem tartalmaz-e olyan adatot, amit nem szeretnél elküldeni.
```

Csak ezután nyissa meg a levelezőprogramot.

### 13.4. SMTP

SMTP-jelszót, SMTP-fiókot vagy SMTP-hitelesítést nem szabad beépíteni az alkalmazásba.

Ha később mégis SMTP-alapú megoldás kellene, az külön, lokális konfigurációból vagy szerveroldali komponensből történjen, nem a kliensprogramba beégetve.

---

## 14. Súgó

A program tartalmazzon offline súgót.

A súgó magyar nyelvű legyen, laikusoknak is érthető.

Tartalom:

1. Mire való a program?
2. Mire nem való a program?
3. Jogszerű használati figyelmeztetés.
4. Link beillesztése.
5. Mentési mappa kiválasztása.
6. Fájlnév megadása.
7. Csak hang letöltése.
8. Videó + hang letöltése.
9. Mappa megnyitása.
10. Letöltés megszakítása.
11. yt-dlp frissítés.
12. Gyakori hibák.
13. Support jelentés küldése.
14. Harmadik féltől származó komponensek.

A súgó lehet:

* beépített HTML oldal,
* Markdownból generált HTML,
* vagy külön `help/` mappa.

Legyenek benne képernyőképek vagy illusztrációk, ahol indokolt.

---

## 15. Névjegy ablak

A Névjegy ablak tartalmazza:

* programnév,
* verziószám,
* build dátum,
* yt-dlp verzió,
* FFmpeg verzió,
* licencinformáció,
* harmadik féltől származó komponensek,
* support e-mail cím.

---

## 16. Verziózás és changelog

Legyen egységes verziókezelés.

Példa:

```text
0.1.0-dev
0.2.0-beta
1.0.0
```

A verzió szerepeljen:

* alkalmazásban,
* Névjegy ablakban,
* build manifestben,
* release notesban.

Legyen:

```text
docs/CHANGELOG.md
```

A changelog minden lényeges változást tartalmazzon.

---

## 17. Build rendszer

### 17.1. Build cél

A build eredménye legyen egy kész, hordozható Windows mappa:

```text
release/TecsoLetolto/
├─ TecsoLetolto.exe
├─ vendor/
│  ├─ yt-dlp/
│  └─ ffmpeg/
├─ help/
├─ licenses/
├─ README_PORTABLE.txt
└─ VERSION.txt
```

Opcionálisan készülhet:

```text
artifacts/TecsoLetolto.zip
artifacts/TecsoLetolto-Installer.exe
```

### 17.2. Build script

Legyen egy fő build script:

```text
scripts/build_release.bat
```

Ez végezze el:

1. régi build maradék törlése;
2. virtuális környezet létrehozása;
3. függőségek telepítése;
4. tesztek futtatása;
5. exe build;
6. vendor komponensek bemásolása;
7. súgó és licencek bemásolása;
8. release mappa ellenőrzése;
9. ZIP elkészítése;
10. build manifest készítése.

### 17.3. Build manifest

Készüljön:

```text
artifacts/build_manifest.json
```

Tartalmazza:

* build időpont,
* git commit hash,
* programverzió,
* Python verzió,
* yt-dlp verzió,
* FFmpeg verzió,
* fájlok listája,
* SHA-256 hash-ek.

---

## 18. Harmadik fél licencek

Készüljön:

```text
docs/THIRD_PARTY_LICENSES.md
release/TecsoLetolto/licenses/THIRD_PARTY_LICENSES.txt
```

Tartalmazza legalább:

* yt-dlp,
* FFmpeg,
* Python / PyInstaller releváns licencinformációk,
* minden egyéb használt könyvtár.

FFmpeg esetén külön ellenőrizni kell, milyen build kerül a csomagba, és annak milyen licencfeltételei vannak.

A Névjegy ablakban legyen utalás arra, hogy a program FFmpeg-et és yt-dlp-t használ.

---

## 19. Tesztek

Legyen legalább alap tesztkészlet.

### 19.1. Unit tesztek

Tesztelendő:

* fájlnév tisztítás,
* dátumos fájlnév generálás,
* fájlnév-ütközés kezelése,
* Letöltések mappa felismerése,
* útvonalkezelés,
* hibaüzenet mapping,
* support jelentés összeállítása,
* verzióadatok olvasása.

### 19.2. Manuális tesztlista

Készüljön:

```text
docs/RELEASE_TEST_CHECKLIST.md
```

Tartalma:

1. Program indul tiszta Windows 10 gépen.
2. Program indul tiszta Windows 11 gépen.
3. Nem kell Python.
4. Nem kell külön FFmpeg.
5. Nem kell külön yt-dlp.
6. Üres célmappa esetén Downloads mappába ment.
7. Üres fájlnév esetén generál nevet.
8. Csak hang mód működik.
9. Videó + hang mód működik.
10. Hibás linkre érthető hibaüzenetet ad.
11. Letöltés megszakítása működik.
12. Mappa megnyitása működik.
13. Support előnézet működik.
14. Levelezőprogram megnyitása működik.
15. yt-dlp frissítés ellenőrzése működik.
16. Naplófájl létrejön.
17. Nem keletkezik szemétfájl a repo gyökerében.
18. A release mappa csak szükséges fájlokat tartalmaz.

---

## 20. Dokumentáció

Frissíteni kell a README-t.

A README ne fejlesztői fókuszú legyen elsődlegesen, hanem felhasználói.

Tartalma:

1. Mi ez?
2. Mire használható?
3. Fontos jogi figyelmeztetés.
4. Gyors használat.
5. Portable verzió indítása.
6. Hang letöltése.
7. Videó letöltése.
8. Frissítés ellenőrzése.
9. Gyakori hibák.
10. Support.
11. Fejlesztői build külön fejezetben.

Fejlesztői dokumentáció külön legyen:

```text
docs/BUILD.md
docs/RELEASE.md
docs/SUPPORT.md
```

---

## 21. AGENTS.md

Készüljön `AGENTS.md`, amely a Codex-agent jövőbeli működési szabályait tartalmazza.

Tartalmazza:

* ne írjon be titkos adatot,
* ne használjon gépspecifikus útvonalat,
* ne tegyen build artifactot forrásmappába,
* release mappába csak kész program kerülhet,
* minden jelentős módosítást dokumentáljon,
* tesztek nélkül ne tekintse késznek a módosítást,
* régi maradékokat ne hagyjon a repóban,
* ha nem biztos valamiben, jelölje `TODO_DECISION` megjegyzéssel és dokumentálja.

---

## 22. STATE.md

Készüljön `STATE.md`.

Tartalma:

* aktuális állapot,
* működő funkciók,
* hiányzó funkciók,
* ismert hibák,
* utolsó audit dátuma,
* következő teendők.

A fejlesztés végén a `STATE.md` ne maradjon elavult.

---

## 23. Régi programmaradékok törlése

A fejlesztés végén kötelező repo-takarítást kell végezni.

### 23.1. Törlendő vagy áthelyezendő maradékok

El kell távolítani vagy új struktúrába kell rendezni:

* régi `.bat` fájlok, ha már nincs szerepük;
* régi `run_gui.bat`, ha az új indítási mód kiváltja;
* régi `run.bat`, ha nincs CLI támogatás;
* beégetett FFmpeg útvonalakat tartalmazó fájlok;
* régi installer script, ha az új build rendszer kiváltja;
* ideiglenes build mappák;
* régi `downloads/` mappa;
* `__pycache__`;
* `.pyc` fájlok;
* régi `.spec` fájlok;
* régi `artifacts/`, ha nem az új buildből származik;
* tesztből visszamaradt médiafájlok;
* lokális naplók;
* `gui_error.log`;
* bármilyen személyes fejlesztői útvonal;
* bármilyen felesleges duplikált dokumentáció.

### 23.2. Tilos törölni ellenőrzés nélkül

Tilos automatikusan törölni:

* licencfájlokat,
* ikonokat,
* dokumentációs forrásokat,
* valóban használt asseteket,
* működő kódrészleteket, amiket az új rendszer is használ.

Előbb listázni kell, mi törlendő és miért.

### 23.3. Takarítás dokumentálása

A takarításról készüljön összefoglaló:

```text
docs/codex-tasks/repo_cleanup_report.md
```

Tartalmazza:

* törölt fájlok,
* megtartott fájlok,
* áthelyezett fájlok,
* indoklás,
* ismert kockázatok.

---

## 24. .gitignore frissítése

A `.gitignore` tartalmazza legalább:

```text
__pycache__/
*.pyc
*.pyo
*.pyd

.venv/
venv/
env/

build/
dist/
*.spec

downloads/
logs/
*.log

artifacts/
release/
installer/_payload/
installer/payload.zip

.env
.env.*
!.env.example

.DS_Store
Thumbs.db
```

Ha a `release/` mappát mégis verziózni akarjuk, akkor külön döntést kell dokumentálni. Alapértelmezés szerint a kész build artifact ne legyen gitben, csak GitHub release-ben vagy artifacts mappában kezelve.

---

## 25. Biztonsági audit

A végén keresni kell a repóban:

```text
password
passwd
secret
token
apikey
api_key
smtp
FFMPEG_DIR
E:\
C:\Users
192.168.
10.
172.16.
```

Minden találatot ellenőrizni kell.

Ha ártalmatlan dokumentációs példa, akkor maradhat, de csak példaként és nem valódi adatként.

---

## 26. Elfogadási feltételek

A feladat csak akkor tekinthető késznek, ha az alábbi feltételek teljesülnek:

1. A program Windows 10/11 x64 alatt Python telepítése nélkül elindul.
2. A program FFmpeg külön telepítése nélkül működik.
3. A program yt-dlp külön telepítése nélkül működik.
4. Nincs beégetett `E:\...` vagy más gépspecifikus útvonal.
5. Nincs beégetett SMTP jelszó, token vagy titkos adat.
6. Van magyar nyelvű GUI.
7. Van link mező.
8. Van mentési mappa mező.
9. Van fájlnév mező.
10. Üres mentési mappa esetén a Windows Letöltések mappába ment.
11. Üres fájlnév esetén biztonságos, dátumos fájlnevet generál.
12. Van “Csak hang” mód.
13. Van “Videó + hang” mód.
14. Van letöltés megszakítása.
15. Van mezők törlése.
16. Van mappa megnyitása.
17. Van tálcára minimalizálás.
18. Van Súgó.
19. Van Support funkció, amely a felhasználó levelezőprogramját nyitja meg.
20. Van Névjegy ablak.
21. Van yt-dlp frissítés ellenőrzése.
22. Van yt-dlp frissítés rollback mechanizmussal.
23. Van érthető magyar hibaüzenet hibás linkre.
24. Van naplózás.
25. Van support jelentés előnézet.
26. Van harmadik fél licencdokumentáció.
27. Van `AGENTS.md`.
28. Van `STATE.md`.
29. Van frissített README.
30. Van build dokumentáció.
31. Van release tesztlista.
32. Van repo cleanup report.
33. A régi, felesleges programmaradékok törölve vagy dokumentáltan áthelyezve vannak.
34. A repó tiszta, áttekinthető, és nem tartalmaz build szemetet.
35. A tesztek futnak.
36. A release csomag ellenőrzése sikeres.

---

## 27. Végső kimenet

A munka végén add vissza az alábbi összefoglalót:

```text
Elvégzett főbb módosítások:
- ...

Új repo struktúra:
- ...

Megmaradt fő fájlok:
- ...

Törölt régi maradékok:
- ...

Build eredmény:
- ...

Teszt eredmény:
- ...

Ismert korlátok:
- ...

Következő javasolt lépések:
- ...
```

A feladat végén ne maradjon félkész állapot, elavult dokumentáció vagy régi indítási logika.

A végső cél: tiszta, laikusbarát, hordozható, magyar nyelvű Windows alkalmazás.
