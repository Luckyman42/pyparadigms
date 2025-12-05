import threading
import time

sem = threading.Semaphore(2)  # egyszerre 2 léphet be

def worker(i: int):
    print(f"Thread {i} start")
    with sem:
        print(f"Thread {i} get semaphore")
        time.sleep(1)
    print(f"Thread {i} done")

threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]

for t in threads: t.start()
for t in threads: t.join()
