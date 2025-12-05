# Asyncio

1 GIL, 1 process, de több coroutine fut: az event loop váltogatja őket.

Context switch nagyon olcsó, mert csak Python stack/Coroutine állapot váltása, nem kernel-level.

Ezért IO-bound-ra kiváló: a CPU sokáig nem blokkolódik, a váltások gyorsak, akár 1000+ coroutine is kezelhető egy processzben.

Nincs párhuzamosság a CPU-n, csak kooperatív konkurencia.

# Threading

1 GIL, 1 process, de több thread: a Python GIL miatt a CPU-bound kód csak egy szálon fut egyszerre, IO-bound kódnál váltanak a thread-ek.

Thread váltás: olcsóbb, mint process switch, de CPU-bound-nál nem skálázódik.

Több thread indítható, de nem érdemes túl sokat, mert GIL miatt a CPU nem tud párhuzamosan dolgozni, és a context switch költség nő.

IO-bound feladatnál hasznos: a várakozó thread-ek alatt a CPU más thread-eket futtat.

# Multiprocessing

Több process, minden processznek saját GIL → valódi párhuzamos futás több CPU-magon.

CPU-bound feladatnál a legjobb választás, mert a GIL nem korlátozza a párhuzamosságot.

Van context switch költség processzek között (CPU állapot mentés, cache flush), és pickle költség, ha adatot kell átadni a processzeknek.

🔹 Összegzés a különbségekről

| Technológia | GIL | Párhuzamosság | Válogatás/Context Switch | Tipikus alkalmazás |
|-------------|-----|----------------|------------------------|-----------------|
| Asyncio | 1 | Nincs, csak konkurencia | Olcsó, Python szintű | IO-bound, pl. API hívások, webszerver |
| Threading | 1 | Nincs CPU-bound-ra, IO-bound-ra jó | Közepes, thread váltás | IO-bound, háttérfeladatok |
| Multiprocessing | Minden process saját | Igen, valódi CPU párhuzam | Drága process switch + pickle | CPU-bound, számítás-intenzív kód |

---


# Asyncio vs Threading vs Multiprocessing
---

| Tulajdonság / Fogalom                 | **Asyncio**                                               | **Threading**                                   | **Multiprocessing**                                                 |
| ------------------------------------- | --------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------- |
| **Futás típusa**                      | Kooperatív konkurencia (coroutine)                        | Preemptív konkurencia (thread-ek)               | Valódi párhuzamosság (process-ek)                                   |
| **GIL**                               | Egy processz, 1 GIL                                       | Egy processz, 1 GIL                             | Minden processz saját GIL                                           |
| **CPU-bound skálázás**                | Nem skálázódik                                            | Nem skálázódik                                  | Teljesen skálázódik, több CPU-magon                                 |
| **IO-bound skálázás**                 | Kiváló, olcsó váltások                                    | Jó, de GIL miatt limitált                       | Jó, de több processz többletköltség                                 |
| **Context switch költség**            | Olcsó, Python szintű (stack/Coroutine)                    | Közepes, kernel-level thread váltás             | Drága, kernel-level process switch + cache flush                    |
| **Pickle / sorosítás**                | Nincs (kivéve run_in_executor ProcessPoolExecutor esetén) | Nincs                                           | Kötelező, ha adatot küldünk processzek között                       |
| **Memória megosztás**                 | Igen, minden coroutine ugyanabban a memóriában            | Igen, thread-ek ugyanazt a memóriát használják  | Nem, minden process saját memóriaterület (shared_memory / IPC kell) |
| **Hibakezelés**                       | Exception a task-ban                                      | Exception thread-ben, nehezebb kezelni          | Future/ProcessPoolExecutor: exception visszakerül                   |
| **Thread/Coroutine indítás költsége** | Nagyon alacsony → akár 1000+ coroutine                    | Közepes, 10–100 thread ideális                  | Magas, process indítás költsége jelentős                            |
| **Tipikus használat**                 | IO-bound, webszerver, API hívások, websocket, DB          | IO-bound, háttérfeladatok, egyszerű konkurencia | CPU-bound, számítás-intenzív kód, párhuzamos számítás               |
| **Hálózati IO**                       | Kiváló, nem blokkol                                       | Jó, de több thread kell                         | Jó, de több processz overhead                                       |
| **Kisebb taskok esetén**              | Nagyon hatékony                                           | Egyszerű, de GIL miatt nem optimalizált         | Pickle és process start overhead miatt drága                        |
| **Nagy adatok átadása**               | Nem probléma                                              | Nem probléma                                    | Pickle-nek köszönhetően lassú lehet, shared memory javasolt         |
| **Egyszerű használat**                | Async/await szintaxis, event loop                         | Thread + Lock/Queue                             | Process + Queue/SharedMemory/Manager                                |
| **Locks / Synchronization**           | Nem szükséges korlátozottan, csak IO-konkurencia          | Lock, RLock, Semaphore, Condition, Barrier      | Lock, Semaphore, Manager, Queue, Pipe                               |
| **Jellemző hibák / rossz praxis**     | CPU-bound feladatok async-n belül → lassú                 | Több thread CPU-bound → GIL miatt lassú         | Kis feladatoknál túl nagy overhead, sok pickle, memóriaköltség      |

---

💡 **Összefoglalás oktatási szempontból:**

* **Asyncio** → IO-bound-ra első számú választás, olcsó context switch, sok coroutine lehet.
* **Threading** → jó IO-bound-ra, CPU-bound-nál nem hatékony, GIL korlátoz.
* **Multiprocessing** → CPU-bound-ra legjobb, valódi párhuzamosság, pickle és process switch költséggel.



# Asyncio vs Threading 

Gyakran az **asyncio** és a **threading** hasonló célokra használható, de van néhány olyan szituáció, amikor **thread-et választunk az asyncio helyett**.

---

### 1️⃣ Asyncio vs Threading – fő különbségek

| Tulajdonság                   | Asyncio                     | Threading                                   |
| ----------------------------- | --------------------------- | ------------------------------------------- |
| Szintaxis                     | async/await, event loop     | Klasszikus szinkron kód, thread-ek          |
| Context switch                | Olcsó, Python szintű        | Közepes, kernel-level                       |
| Skálázhatóság IO-bound-ra     | Nagyon jó (1000+ coroutine) | Jó, de túl sok thread drága                 |
| CPU-bound                     | Nem jó                      | Nem jó CPU-bound-ra sem, GIL miatt          |
| Külső blokkoló kód            | Async wrapper szükséges     | Egyszerűen fut, nincs async konverzió       |
| Külső könyvtár kompatibilitás | Csak async könyvtárakkal    | Bármit használhatsz, akár blocking kódot is |

---

### 2️⃣ Mikor érdemes **thread-et választani**?

1. **Ha a meglévő kód blokkoló, szinkron, nem lehet egyszerűen async-re konvertálni**

   * Pl. régi könyvtárak, amelyek szinkron I/O-t csinálnak (pl. `requests` HTTP könyvtár, nem `aiohttp`).
   * Asyncio-val akkor wrapper kell (`run_in_executor`), ami overhead, thread-del egyszerűen fut.

2. **Ha a task rövid, egyszerű, de mégis párhuzamosítani akarjuk**

   * Nem kell komplex event loop kezelése.
   * Pl. kis background task-ok, log feldolgozás, file I/O.

3. **Ha a kód keveri a CPU és IO munkát, de nem akarjuk a teljes async kódot megírni**

   * Thread-ekkel lehet könnyen elindítani néhány párhuzamos munkát anélkül, hogy minden async legyen.

4. **Ha a cél a kompatibilitás és egyszerűség**

   * Asyncio-t tanulni kell, és minden függvény async/await legyen.
   * Threadinghez a legtöbb szinkron kód kompatibilis, egyszerű lock-okkal, Queue-val.

---

### 4️⃣ Összefoglalás

* **Asyncio** → nagy számú, IO-bound, modern async könyvtárakkal.
* **Threading** → meglévő blokkoló kód párhuzamosítására, könnyen használható, kompatibilis minden könyvtárral.
* **Nyertes use case thread-re**: meglévő szinkron könyvtárak, rövid task-ok, könnyű párhuzamosítás, nem akarjuk teljesen átírni az alkalmazást async-re.

---
