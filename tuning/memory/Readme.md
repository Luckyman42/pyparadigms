# 🧠 Python Memory Model, Arena Fragmentation & Long-Running Server Stability

## For FastAPI / Uvicorn / Gunicorn on Kubernetes

---

## CPython Memory Model Overview

Python uses a layered allocator:

```
Object → PyObject Allocator → Small Object Allocator → Arenas → OS
```

### **Key components**

| Layer                                 | Description                                          |
| ------------------------------------- | ---------------------------------------------------- |
| **Small Object Allocator (pymalloc)** | Used for objects ≤ 512 bytes                         |
| **Arenas**                            | Fixed **256 KB** memory chunks requested from the OS |
| **Pools**                             | Arenas contain pools for different object sizes      |
| **OS Allocator**                      | `malloc()` / `mmap()` underneath                     |

### **Important behavior**

* Python **never returns arenas back to the OS** until the process exits.
* Even if objects inside an arena are deleted,
  **the arena stays reserved** → memory stays high.

This is known as **arena fragmentation**.

#### Fragmentation

-   Memory gets fragmented because arenas **are never returned to the
    OS**
-   Even if objects are deleted, memory may remain allocated
-   Long-running processes (e.g., FastAPI) show memory growth over time


---


## Memory Behavior in Threading, Multiprocessing, Web Servers

### Threading

-   Threads share the same memory space
-   Memory fragmentation accumulates
-   Memory leaks affect the entire process

### Multiprocessing

-   Each process has its own memory space
-   Better for avoiding fragmentation buildup
-   Allows true parallelism (bypasses GIL)

### Webserver (FastAPI/Uvicorn)

-   Each worker is a separate process in:
    -   `uvicorn --workers N`
    -   `gunicorn -k uvicorn.workers.UvicornWorker -w N`
-   Requests inside the same worker **share the same heap**
-   Long-running workers grow memory over time


## The Problem in Long-Running Systems (FastAPI, background jobs, workers)

### What causes memory to “grow but never shrink”?

1. Your code temporarily allocates many Python objects:

   * large lists
   * temporary dicts
   * JSON parsing
   * database result sets
   * big NumPy → Python conversions

2. Python allocates new pools & arenas.

3. Even if you delete all temporary objects:

   ```
   del data
   gc.collect()
   ```

   → **arenas remain allocated**, because Python cannot return them to the OS.

### Result:

➡️ Memory footprint only goes **up**, never down.
➡️ In Kubernetes, this eventually hits the **container memory limit**
➡️ OOM Kill → pod restarts unexpectedly.

---

## 3. Standard Solution: Worker Rotation

Because memory won’t drop until the process exits:

### 🔥 The only reliable fix:

**Restart the Python process periodically.**

Examples:

* Gunicorn `--max-requests`
* Uvicorn workers inside Gunicorn (`uvicorn.workers.UvicornWorker`)
* Kubernetes lifecycle + livenessProbe memory check

This prevents unbounded growth caused by fragmentation.

---

## 4. Mitigation Technique: In-Place Operations

*(Useful but dangerous if misused)*

### Why it helps

If you modify existing Python structures **in place**,
Python does **not** need to allocate new arenas.

Example (Safer):

```python
# avoids allocating a new list
for i in range(len(values)):
    values[i] *= 2
```

Example (Dangerous: allocates new objects):

```python
values = [x * 2 for x in values]   # new list, new arenas potentially
```

### ⚠️ Risks of in-place optimization

* Mutating shared objects leads to subtle bugs:

  * unexpected side effects
  * thread safety issues
  * corrupted state in async applications
* Harder to maintain and test
* Does NOT eliminate all fragmentation sources

Use this only in **hot paths** where performance matters.

---

## 5. Practical Example: Avoid Excess Allocations

### ❌ Bad (creates new objects + new arenas)

```python
def scale(values):
    return [v * 1.5 for v in values]
```

### ✔️ Better (in-place)

```python
def scale_inplace(values):
    for i in range(len(values)):
        values[i] *= 1.5
    return values
```

Still, fragmentation may occur in other parts of the code.

---

## 6. Gunicorn + Uvicorn Worker Setup (Recommended for FastAPI)

### **Gunicorn configuration (Python file)**

`gunicorn_conf.py`

```python
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
max_requests = 2000
max_requests_jitter = 400
timeout = 60
```

### **Start command**

```bash
gunicorn -c gunicorn_conf.py main:app
```

This ensures:

* worker auto-restart every 2000–2200 requests
* memory never grows unbounded
* stable behavior under load

---

## 7. Pure Uvicorn (less isolation, not recommended for production)

```bash
uvicorn main:app \
  --workers 4 \
  --limit-max-requests 2000 \
  --limit-max-requests-jitter 200
```

Note: pure Uvicorn worker rotation is **not as robust** as Gunicorn’s.

---

## 8. Kubernetes Memory Safety Strategy

### Sample livenessProbe using a memory check

```python
# /app/healthcheck.py
import psutil
import sys

LIMIT_MB = 500
main = psutil.Process(1)
rss_mb = main.memory_info().rss / (1024**2)

if rss_mb > LIMIT_MB:
    sys.exit(1)  # fail liveness probe → restart
sys.exit(0)
```

### probe config

```yaml
livenessProbe:
  exec:
    command: ["python", "/app/healthcheck.py"]
  initialDelaySeconds: 10
  periodSeconds: 20
```

Because the probe runs in the **same container & PID namespace**,
it can read the memory usage of the main process.

---

# ✅ Summary

| Topic                                | Explanation                                                  |
| ------------------------------------ | ------------------------------------------------------------ |
| **Arena fragmentation**              | Python allocates 256 KB arenas and never returns them to OS  |
| **Memory grows permanently**         | Even after `del` and `gc.collect()`                          |
| **Long-running apps leak by design** | Not a bug — CPython allocator behavior                       |
| **Solution**                         | Worker rotation (Gunicorn max-requests, Kubernetes restarts) |
| **In-place ops**                     | Can reduce arena churn but risky                             |
| **Uvicorn/Gunicorn**                 | Best way to run FastAPI with stable memory                   |
