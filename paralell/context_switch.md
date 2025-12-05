
### 1️⃣ Mi történik a **process context switch** során?

* Amikor az OS vált egy **processzről egy másik processzre** ugyanazon CPU-magban:

  * A CPU állapotát menteni kell (regiszterek, stack pointer, program counter).
  * A másik processz állapotát betölteni.
  * Gyakran cache flush is történik, mert az új processz más memóriaterületeket használ.
* **Az idő, ami itt elmegy**, az a context switch költség.
* Ha a process nagy memóriaterületeket használ (sok stack, sok adat), akkor a CPU cache invalidálása és a memória elérése miatt a költség nagyobb lehet.

---

### 2️⃣ Mi történik **thread váltásnál a GIL miatt** Pythonban?

* Pythonban a GIL miatt **egy CPU-magon egyszerre csak egy szál futhat**.
* Ha a GIL átadódik egy másik szálnak:

  * A CPU állapot mentése ugyanúgy történik (registerek, stack pointer).
  * A szál lokális változóit, stack-jét kell betölteni.
  * A Python GIL váltás **olcsóbb**, mint a teljes process switch, de CPU-bound feladatnál ez mégis overhead.
* IO-bound kódnál a szálak sokszor várakoznak, így a context switch költség **elenyésző**.

---

### 3️⃣ Multiprocessing előnye CPU-bound esetén

* Minden processz **saját Python interpreter + saját GIL**, tehát **ténylegesen párhuzamosan futhat több magon**.
* Emiatt a CPU-bound munkát **több CPU-mag egyszerre végzi**, így a thread váltás okozta context switch költséget jelentősen csökkentjük.
* Természetesen minden processznek saját memóriaterülete van → **pickle/IPC költségek** lehetnek, de a tényleges számítás gyorsabb lesz.

---

💡 **Összegzés**:

* **Egy CPU-magon**: process vagy thread váltás → context switch költség (CPU állapot mentés/beolvasás + cache flush).
* **Thread IO-bound**: kevésbé számít, mert sokat várakozik.
* **Thread CPU-bound**: költséges, mert GIL miatt nincs párhuzam.
* **Multiprocess CPU-bound**: lehet párhuzamos több magon → hatékonyabb, kevesebb context switch overhead a számítás szempontjából.

