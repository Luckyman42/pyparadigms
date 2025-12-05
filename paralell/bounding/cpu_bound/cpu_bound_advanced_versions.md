# CPU-bound Feladat — Haladó Megoldások (Frissített, Tiszta Verzió)

Ebben a dokumentumban a CPU-bound feladathoz mutatjuk a "haladó", ajánlott és demonstrációs megoldásokat:

- **ProcessPoolExecutor** — ajánlott Python CPU-bound kód párhuzamosítására.
- **asyncio + run_in_executor (ProcessPoolExecutor)** — ha az alkalmazás főként async, de van CPU-bound munka.
- **ThreadPoolExecutor** — demonstráció: miért nem jó CPU-boundra.

---

# Alapadatok
```python
N = 4       # párhuzamos feladatok száma
FIB_N = 30  # Fibonacci szám, ami CPU-intenzív
```

---

# 1️⃣ ProcessPoolExecutor (ajánlott CPU-boundra)

[Kód](advanced_process_solution.py)

**Előnyök:**
- A GIL nem akadályozza a párhuzamos futást
- Könnyű kezelni és hibakezelhető Future-ök segítségével
- Skálázható CPU-intenzív feladatokra

---

# 2️⃣ Asyncio + run_in_executor (ProcessPoolExecutor)
Ha az alkalmazás főként async, és kell CPU-intenzív munka, offloadoljuk process pool-ba.

[Kód](advanced_async_solution.py)

**Előnyök:**
- Async alkalmazás fő része nem blokkolódik
- CPU-munka párhuzamosan fut több processzben

---

# 3️⃣ ThreadPoolExecutor (demonstráció — nem CPU-bound-ra)

[Kód](advanced_thread_solution.py)

**Megjegyzés:**
- A GIL miatt a futásidő nem csökken jelentősen
- Jó demonstráció arra, hogy miért nem szabad CPU-intenzív feladathoz thread pool-t használni

---

# Összegzés
| Megközelítés | CPU-boundra jó? | Ajánlás |
|-------------|----------------|---------|
| ProcessPoolExecutor | Igen | Használd CPU-intenzív Python kódhoz |
| asyncio+run_in_executor | Igen | Ha async app és kell CPU munka |
| ThreadPoolExecutor | Nem | Ne használd csak CPU-boundra |

