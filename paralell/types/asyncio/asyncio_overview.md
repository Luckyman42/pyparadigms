# Asyncio – Oktatási Áttekintés (Python 3.13)

## 1. Mi az asyncio és mire jó?
Az `asyncio` Python beépített keretrendszere **aszinkron, egy szálon futó, kooperatív konkurencia** megvalósítására. Elsősorban:
- **IO‑bound** feladatokra jó,
- ahol az idő nagy részét **külső eszközre várakozás** teszi ki (hálózat, fájl, adatbázis),
- és sok egyidejű kapcsolat/feladat van.

Nem alkalmas:
- CPU‑intenzív kód párhuzamos futtatására,
- hosszú, blokkoló műveletekhez.

---

## 2. Event Loop belső működése
Az event loop lépései:
1. összegyűjti a futtatásra kész taszkokat,
2. kiválasztja a következő awaitable objektumot,
3. átadja neki a vezérlést,
4. amikor az awaitel egy IO műveletre, a loop felfüggeszti,
5. ha az IO befejeződik, visszaütemezi.

A loop **kooperatív**: csak akkor adja vissza a vezérlést, ha a kód `await`-tel átadja.

Ezért a blokkoló műveletek „lefagyasztják” az egész event loopot.

---

## 3. Task scheduling és az Awaitable protokoll
### Awaitable protokoll
Egy objektum awaitelhető, ha:
- `__await__()` metódust implementál,
- vagy `async def` által létrehozott coroutine.

### Task scheduling
- `asyncio.create_task(coro)` → a coroutine futása taszkká alakul.
- A taszkot a loop ütemezi.
- A taszk állapotai: **pending → running → suspended → done**.

---

## 4. uvloop
Az `uvloop` egy alternatív, extrém gyors event loop (libuv alapokon).

Használata:
```python
import uvloop
import asyncio

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
```

Előnyök:
- sokkal gyorsabb IO műveletek,
- alacsonyabb latencia,
- jobb skálázódás.

---

## 5. Cancellation, Timeout, Shield
### Cancellation
Egy task leállítható:
```python
task.cancel()
```
A coroutine `CancelledError` kivételt kap.

### Timeout
```python
await asyncio.wait_for(coro, timeout=2.0)
```

### Shield
Megakadályozza, hogy a külső timeout/cancel törölje a feladatot.
```python
await asyncio.shield(coro)
```

---

## 6. Structured Concurrency – TaskGroup
Python 3.11+ egyik legfontosabb újítása.

```python
async with asyncio.TaskGroup() as tg:
    t1 = tg.create_task(fetch_data())
    t2 = tg.create_task(process_data())
```

**Garanciák:**
- minden task vagy sikeresen lefut, vagy hiba esetén **mind** megszakad,
- nincs „szabadon lógó” task,
- könnyebb hibakezelés és erőforrás‑menedzsment.

---

## 7. Mikor jó az asyncio?
### Ajánlott, ha:
- sok egyidejű IO kapacitás kell
- websocket szerver / kliens
- HTTP kliens
- adatbázis aszinkron driver
- proxyk, gatewayek, mikroservice kommunikáció

### Nem ajánlott:
- CPU‑igényes számítás
- képfeldolgozás, ML, tömörítés
- kriptográfia

Ezekhez a `multiprocessing` vagy `concurrent.futures.ProcessPoolExecutor` való.

