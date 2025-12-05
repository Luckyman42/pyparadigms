## **1️⃣ Az Event Loop alapjai**

Az **event loop** az `asyncio` alapja. Fő feladata, hogy **kooperatívan váltogassa a futó coroutine-okat**, kezelje az IO eseményeket és a callback-eket.

### Feladatai:

1. **Folyamatban lévő coroutine-ok ütemezése**:

   * Minden `async def` függvény coroutine objektummá válik.
   * Az event loop figyeli, hogy melyik coroutine **await-nél blokkolódik** (pl. `await asyncio.sleep()` vagy IO).
   * Ha a coroutine await-nél vár, az event loop a következő futtatható coroutine-t választja.

2. **IO események figyelése**:

   * Az event loop egy **non-blocking IO multiplexer**-ként működik (`select`, `poll`, `epoll` Linuxon, `kqueue` macOS).
   * Például ha van egy socket, amely olvasásra vár, az event loop regisztrálja az eseményt.
   * Amikor az OS jelzi, hogy az IO kész, az event loop futtatja a hozzá tartozó callback-et vagy coroutine-t.

3. **Callback-ek, timeouts, scheduled tasks kezelése**:

   * Pl. `loop.call_later()`, `loop.call_at()`.
   * Az event loop egy **prioritási queue-t** használ az időzített callback-ekhez.

4. **Task scheduling**:

   * A `Task` wrapper korutin számára: a loop feladata a Task-ok futtatása, await pontnál felfüggesztés, újraindítás.
   * Ez a **kooperatív multitasking** alapja: a váltás csak await vagy yield pontokon történik.

---

## **2️⃣ Belül hogyan működik**

1. **Futó coroutine-ok listája (ready queue)**:

   * A loop tart egy listát (`_ready`) a futásra kész task-okról.
   * Minden iterációban (`loop.run_forever()`) a loop végigmegy a `_ready` task-okon, futtatja őket.

2. **IO multiplexing**:

   * A loop egy `selector`-t használ (`selectors.DefaultSelector`), ami platformfüggő:

     * Linux: `epoll`
     * macOS: `kqueue`
     * Windows: `IOCP`
   * A selector figyeli a file descriptor-okat, jelez, ha olvasható/írható.

3. **Kooperatív multitasking**:

   * A váltás **nem preemptív**: a coroutine saját maga felfüggeszti magát `await`-nél.
   * Ezért a context switch **nagyon olcsó**, nincs kernel-level váltás, csak Python stack mentés.

4. **Timeout és cancel kezelés**:

   * A loop figyeli az időzített feladatokat, ha lejár a timeout, exception dobódik a coroutine-ban.
   * `Task.cancel()` értesíti a loop-ot, hogy a következő iterációban dobja a `CancelledError`-t.

---

## **3️⃣ Mi az `uvloop` és miért gyorsabb?**

* `uvloop` egy **alternatív event loop implementáció**, teljesen Cython/C implementációval.
* Alapja az **libuv** könyvtár (ugyanaz, amit a Node.js használ).
* Előnyei:

  1. **Sebesség**: sokszor 2–5x gyorsabb, mert a loop teljesen C szintű, nincs Python overhead.
  2. **Hatékony IO multiplexing**: libuv optimalizált az epoll/kqueue/IOCP használatra.
  3. **Jobb skálázás nagy számú socket/fájl descriptor esetén**.
* Használata egyszerű:

  ```python
  import asyncio
  import uvloop

  asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
  ```
* Belsőleg ugyanazokat az elveket követi:

  * ready queue
  * selector
  * callback/task scheduling
* De a Python-szintű overhead minimalizálva van, így **nagyon gyors váltások és IO-kezelés**.

---

## **4️⃣ Összegzés az oktatáshoz**

| Fogalom              | `asyncio` default loop        | `uvloop`                             |
| -------------------- | ----------------------------- | ------------------------------------ |
| Implementáció        | Python + C                    | Teljes C/libuv                       |
| IO multiplexing      | selectors (epoll/kqueue/IOCP) | libuv                                |
| Coroutine scheduling | Python Task-ok, ready queue   | Ugyanaz, gyorsabb C implementáció    |
| Context switch       | Python stack mentés, olcsó    | Ugyanaz, de gyorsabb és skálázhatóbb |
| Sebesség             | Jó                            | Gyors, 2–5x jobb nagy terhelésnél    |

