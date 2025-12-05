import threading
import time

barrier = threading.Barrier(3)

def task(i : int ):
    print(f"Thread {i} start")
    time.sleep(2+i)
    print(f"Thread {i} wait for barrier...")
    barrier.wait()
    print(f"Thread {i} done")

threads = [threading.Thread(target=task, args=(i,)) for i in range(3)]

for t in threads: t.start()
for t in threads: t.join()
