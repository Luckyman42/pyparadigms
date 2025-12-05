# 🧵 **1) Daemon Thread – mi ez és mi történik vele?**

### ✔️ **A daemon thread egy “háttérszál”, amelyet a Python NEM vár meg kilépéskor.**

Ha **minden nem-daemon** thread lefutott,
**a program AZONNAL kilép**,
és **minden daemon threadet kíméletlenül megöl**.

### ➤ Daemon thread tipikus használata:

* háttér loggolás
* monitorozás
* watchdog
* periodikus ellenőrzések

### ➤ Daemon thread nem alkalmas:

* fontos munkára!
* resource cleanup-ra
* fájl írására → félbemarad

### Példa – daemon thread megszakad programkilépéskor

```python
import threading
import time

def worker():
    for i in range(10):
        print("daemon working", i)
        time.sleep(0.5)

t = threading.Thread(target=worker, daemon=True)
t.start()

print("Main thread ends → daemon killed.")
```

**Output:**

* Néhány sor után → program kilép
* Daemon thread **félbeszakad**

---

# 🧵 **2) Daemon Thread fő szabályai:**

* `t.daemon = True` → *mielőtt* `start()`-ot hívod
* main thread nem várja meg
* ha utolsó nem-daemon thread véget ér → daemonok *instant halál*
* nem garantált cleanup

---

# 🔥 **3) Daemon Process (multiprocessing) – miben más?**

### ✔️ Daemon process = olyan subprocess, amely:

* **nem spawn-olhat új folyamatot**
* **nem használhat pool-t**
* **a parent process halálakor automatikusan leáll**
* **nem biztonságos cleanupra**

A fő különbség: **daemon process HARD STOP-pal hal meg**, nem szál-szerűen.

### Példa – daemon process

```python
from multiprocessing import Process
import time

def worker():
    for i in range(10):
        print("daemon proc", i)
        time.sleep(0.5)

p = Process(target=worker)
p.daemon = True
p.start()

print("Main ends → daemon process is killed.")
```

### A különbség a threadhez képest?

* Bizonyos platformokon **azonnal SIGKILL**, nincs cleanup
* Nem indíthatsz belőle új process-t → hiba:

```
AssertionError: daemonic processes are not allowed to have children
```

---

# 🔍 **4) A legfontosabb különbségek egy táblázatban**

| Tulajdonság                      | Daemon Thread                                       | Daemon Process                              |
| -------------------------------- | --------------------------------------------------- | ------------------------------------------- |
| Megvárja-e a runtime kilépéskor? | ❌ Nem                                               | ❌ Nem                                       |
| Hogyan hal meg?                  | szál-szerűen, erővel                                | process szinten: SIGKILL / terminate        |
| Clean-up esély?                  | kicsi                                               | még kisebb                                  |
| Indíthat-e gyereket?             | ✔️ igen                                             | ❌ NEM                                       |
| Join-olható?                     | tudsz join-t hívni, de nem garantált hogy végigmegy | join fut, de process meghal, nem fejezi be  |
| Tipikus használat                | háttérszál                                          | watchdog process / nem kritikus háttérmunka |

---

# 🔥 **5) Miért veszélyesek a daemonok?**

### Daemon thread veszélyek:

* félépő fájl-írás
* nem flush-ölt buffer
* resourcerek nyitva maradnak (pl socket)
* log félbemarad

### Daemon process veszélyek:

* all child processes tiltva
* socket/file cleanup hiányzik
* shared memory korrupt lehet
* nem lehet pool-ból használni

---

# 🧠 **6) Egyszerű szabály:**

### ✔️ “Ha fontos a feladat → SOHA ne legyen daemon.”

Daemon = *“csak ha lényegtelen, hogy befejezi-e”*.

---

# ✔️ Összefoglalás

### **Daemon thread**

* csak addig fut, amíg nem marad más nem-daemon thread
* main kilépése **megöli**

### **Daemon process**

* még szigorúbb:

  * nem hozhat létre subprocess-t
  * parent kilépése = daemon kill
* nem használható Pool-lal
