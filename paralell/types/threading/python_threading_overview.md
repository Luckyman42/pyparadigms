# Threading 

A `threading` modul a Python beépített eszköze **szálak** kezelésére. A szálak egy folyamaton belül futnak, közös memóriát használnak, és elsősorban **IO-bound** feladatok párhuzamosítására alkalmasak.

---

# 1. Mire jó a threading és mire nem?
## Jó választás:
- IO-bound feladatok (hálózat, fájl, API-hívások)
- Sok, kis várakozást tartalmazó művelet
- Olyan rendszerek, ahol külső API-ra várakozás a domináns

## Rossz választás:
- CPU-bound számítás (a GIL miatt)
- Nagy számú szál létrehozása (overhead + context switching költség)

A GIL (Global Interpreter Lock) korlátozza a Python szálait: **egy folyamatban egyszerre csak egy szál fut ténylegesen Python bytecode-ot**.

IO-bound feladatoknál viszont a blokkoló műveletekre várakozás alatt a GIL felszabadul.

---

# 2. Szinkronizációs primitívek

## 2.1 Lock
Az alapvető kölcsönös kizárást biztosító primitív.

```python
lock = threading.Lock()
with lock:
    critical_section()
```

## 2.2 RLock (Reentrant Lock)
Ugyanaz, mint a Lock, de ugyanaz a szál többször is megszerezheti.

```python
lock = threading.RLock()
```

## 2.3 Condition
Szálak közötti értesítési mintákhoz.

```python
cond = threading.Condition()
with cond:
    cond.wait()
    cond.notify_all()
```

## 2.4 Semaphore
Erőforrások számát korlátozza.

```python
sem = threading.Semaphore(3)
```

## 2.5 Barrier
Szinkronizál több szálat egy közös ponton.

```python
barrier = threading.Barrier(5)
barrier.wait()
```

---

# 3. ThreadPoolExecutor belső működése
A `ThreadPoolExecutor` a `concurrent.futures` része.

### Fő elemei:
- Egy fix vagy dinamikus számú munkaszál
- Egy feladat queue
- Munkaszálak, melyek a queue-ból dolgoznak
- A GIL miatt **egy időben csak egy Python bytecode fut**, de IO esetén felszabadul

Előnye:
- egyszerű API
- saját queue-t és munkaszálakat kezel

```python
from concurrent.futures import ThreadPoolExecutor

def work(x):
    ...

with ThreadPoolExecutor(max_workers=10) as exe:
    futures = exe.map(work, range(100))
```

---

# 4. Memory Visibility (Happens-Before)
A Python GIL **nem garantál memóriaszinkronizációt** a szálak között!

Például:
- egy szál ír egy változóba,
- a másik olvassa,
- de a CPU cache vagy fordítási optimalizáció miatt nem biztos, hogy azonnal látja.

Erre **szinkronizációs primitíveket** kell használni (Lock, Event, Condition), amelyek:
- *happens-before* kapcsolatot hoznak létre.

```python
# Helyes minta
with lock:
    shared_state += 1
```

---

# 5. Mikor használjunk threadinget?
## Használd threadinget, ha:
- IO-bound feladatokat akarsz párhuzamosítani
- egyszerű API kell (ThreadPoolExecutor)
- kevés szál is elég
- nem baj a GIL limitáció

## Ne használd threadinget, ha:
- CPU-intensive feladatod van → multiprocessing kell
- sok szálra lenne szükség (1000+) → async IO vagy multiprocessing jobb
- determinisztikus, alacsony-latenciás ütemezés kell

---

# 6. Példák

## 6.1 Egyszerű szálindítás
```python
import threading

def worker():
    print("Hello from thread!")

th = threading.Thread(target=worker)
th.start()
th.join()
```

## 6.2 Lock használata
```python
lock = threading.Lock()
count = 0

def inc():
    global count
    for _ in range(1000):
        with lock:
            count += 1
```

## 6.3 Condition példa
```python
condition = threading.Condition()
ready = False

def waiter():
    with condition:
        condition.wait_for(lambda: ready)
        print("Go!")

def setter():
    global ready
    with condition:
        ready = True
        condition.notify_all()
```

