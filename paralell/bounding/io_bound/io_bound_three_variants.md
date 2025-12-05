# IO-bound Feladat — Három Technológia (Asyncio, Threading, Multiprocessing)

Ez a dokumentum egy **nagyon egyszerű**, oktatásra optimalizált verziója a háromféle IO-bound párhuzamosításnak.  
**Nem használunk TaskGroup / Executor / Pool megoldásokat az első példákban**, csak a *legtisztább* alap működést.  
Később *ugyanarra* mutatunk egy „jobb” verziót is, és elmagyarázzuk a különbséget.

---

# 🌐 A feladat
Töltsünk le **20 URL-t** (késleltetett 1 másodperces válasszal).  
A végén szó lesz arról, mi történik **N = 100** esetén.

```python
URL = "https://httpbin.org/get"
N = 20
```

---

# 1️⃣ ASYNCIO — alap verzió (jó választás)
Ez a *legletisztultabb* IO-bound megoldás.

[Kód](basic_async_solution.py)

## Miért jó?
- tökéletesen skálázódik (1000+ kérést is bír)
- alacsony context switching költség
- nem hozunk létre szálakat

---

# 2️⃣ THREADING — alap verzió (jó, de nem optimális)
A Python szálak jól működnek IO-bound feladatnál, de **nem skálázódnak olyan jól**, mint az asyncio.

[Kód](basic_thread_solution.py)

## Miért működik, de nem a legjobb?
- 20 szál még oké → **100 szál már lassú és instabil lehet**
- nagy context switching költség
- több memóriahasználat szálanként

---

# 3️⃣ MULTIPROCESSING — alap verzió (rossz választás)
IO-bound feladatnál mindig rossz.  
A folyamatok közötti kommunikáció (IPC), a forkolás és a pickle költség felesleges.

[Kód](basic_process_solution.py)

## Miért rossz?
- minden processz külön memória → óriási overhead
- nagyon lassú indulás (`fork`)
- az eredményt nem is lehet így helyesen összegyűjteni (`results` nem shared!)
- 20 processz még elmegy — **100 processz már halál biztos**

---

# 📊 Mi történik N = 100 esetén?
| Technológia | Eredmény | Magyarázat |
|-------------|----------|------------|
| **asyncio** | gyors | egy event loop elbír 1000+ kapcsolatot is |
| **threading** | közepes/lassú | 100 szál még elmegy, de sok context switching és memória |
| **multiprocessing** | nagyon lassú / instabil | 100 processz óriási overhead |

---

# 📚 Összegzés
| Technológia | IO-boundra jó? | Miért? |
|-------------|----------------|--------|
| **asyncio** | ⭐⭐⭐⭐⭐ | egyetlen thread, kooperatív, skálázódik |
| **threading** | ⭐⭐⭐⭐ | működik, de több overheaddel |
| **multiprocessing** | ⭐ | nem való IO-boundra (fork + pickle + memória költség) |


