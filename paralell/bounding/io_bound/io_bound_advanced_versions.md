# IO-bound Feladat — Haladó Megoldások

Ebben a dokumentumban ugyanarra az IO-bound feladatra (20 db 1s késleltetett HTTP kérés) bemutatjuk a **haladó**, "szép" megoldásokat mindhárom technológiára:

- `asyncio` → **TaskGroup**
- `threading` → **ThreadPoolExecutor**
- `multiprocessing` → **ProcessPoolExecutor** (csak demonstráció, továbbra is rossz IO-bound-ra)

A cél: megmutatni, hogy néz ki a *helyes, stabil, skálázható* forma, ahol pool-ok újrahasznosítják az erőforrásokat.

---

# 🌐 Alapadatok
```python
URL = "https://httpbin.org/get"
N = 20
```

---

# 1️⃣ Asyncio — TaskGroup (helyes + modern + skálázható)

A Python 3.11+ óta elérhető a **TaskGroup**, ami struktúrált konkurenciát ad.

[Kód](advanced_async_solution.py)


## Előnyök
- jól strukturált
- kiváló hibakezelés (egy task hibája leállítja a csoportot, nem maradnak "zombi taskok")
- könnyen skálázódik több száz vagy ezer feladatra

---

# 2️⃣ Threading — ThreadPoolExecutor (jó választás IO-boundra)
A **ThreadPoolExecutor** újrahasznosítja a szálakat, így nem kell 20–100 új szálat létrehozni.

[Kód](advanced_thread_solution.py)

## Előnyök
- sokkal kisebb overhead, mint 20–100 szál létrehozása
- a pool mérete kontrollálható → nem lőjük szét a rendszert
- egyszerű és érthető

---

# 3️⃣ Multiprocessing — ProcessPoolExecutor (rossz IO-bound feladatra)
Csak demonstráció: ez működik, de **lassabb**, **több memóriát eszik**, és **teljesen felesleges** hálózati IO-ra.

[Kód](advanced_process_solution.py)

## Miért rossz?
- minden feladat pickle-elve kerül át a másik processzbe
- minden processz saját Python interpretert futtat
- nagy indulási költség (fork/spawn)
- teljesen fölösleges IO-bound feladatnál

---

# 📌 Összegzés
| Technológia | Haladó forma | IO-bound-ra jó? | Megjegyzés |
|-------------|--------------|----------------|-------------|
| **asyncio** | TaskGroup | ⭐⭐⭐⭐⭐ | A legjobb megoldás |
| **threading** | ThreadPoolExecutor | ⭐⭐⭐⭐ | Jó, amíg nem extrém sok a feladat |
| **multiprocessing** | ProcessPoolExecutor | ⭐ | Csak rossz példa, hogy miért nem ez kell IO-ra |
