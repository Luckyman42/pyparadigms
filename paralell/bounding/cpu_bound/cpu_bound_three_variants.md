# CPU-bound feladat — Három egyszerű megvalósítás

Feladat: számoljuk ki többször egy nehezebb számítási feladatot — naiv Fibonacci rekurzióval. Ez **CPU-bound** példa: a GIL számítás közben korlátozza a thread-eket, ezért a multiprocessing a helyes eszköz.

---

# 🌐 Alapadatok (beégetve)
```python
# Módosítható: de alapban ezek maradnak
N = 4        # hány párhuzamos feladatot indítunk
FIB_N = 30   # milyen 'n'-re számoljuk a Fibonacci-t

# Megjegyzés: FIB_N=30 viszonylag lassú, okul: FIB_N=35 már jelentősen lassabb lehet.
```

---

# 1️⃣ ASYNCIO — alap verzió (ROSSZ praxis CPU-boundra)
Ez a példa megmutatja, hogy **az asyncio nem csodaszer CPU-bound kódra** — ha simán `await`-oljuk a szinkron függvényt, a GIL miatt nem fog párhuzamosan futni.

[Kód](basic_async_solution.py)

## Mit tanít ez meg?
- A kód "concurrent"-nek tűnik, de a GIL miatt **nem fog skálázódni** CPU magokra.
- Használhatjuk demonstrációnak, de ne ajánljuk productionben.

---

# 2️⃣ THREADING — alap verzió (ROSSZ praxis CPU-boundra)
A szálak sem segítenek Pythonban CPU-intenzív feladatoknál a GIL miatt — ez a példa ezt demonstrálja.

[Kód](basic_thread_solution.py)

## Mit tanít ez meg?
- Látható, hogy a futási idő nem javul érdemben a több szál használatával.
- Jó demonstráció, hogy miért nem a thread a megoldás CPU-boundra.

---

# 3️⃣ MULTIPROCESSING — alap verzió (HELYES megoldás)
A folyamatoknak saját interpreterük van, így a GIL nem korlátozza őket. Itt a `multiprocessing` a megfelelő eszköz.

[Kód](basic_process_solution.py)

## Mit tanít ez meg?
- A futási idő jelentősen lerövidül, mert a számítás párhuzamosan fut több CPU-magon.
- Manager-lista használata egyszerűbb megoldás az eredmények összegyűjtésére.

---

# 📊 N = 8 vagy FIB_N növelése esetén
- **asyncio / threading**: a futásidő linearitása nem javul, sőt overhead miatt rosszabbodhat.
- **multiprocessing**: jellemzően jól skálázik, de figyelj a processz indítási költségre és a memóriahasználatra.

