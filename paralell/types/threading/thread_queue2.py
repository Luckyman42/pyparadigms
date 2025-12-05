import threading
from queue import Queue, Empty
import time

def producer(q : Queue[int|None]):
    for i in range(5):
        q.put(i)
        print(f"Produce: {i}")
        time.sleep(1)
    q.put(None)
    print("Producer done")

def consumer(name : str, q: Queue[int|None]):
    while True:
        try:
            item = q.get(timeout=5)
        except Empty:
            print("Timeout over")
            break
        if item is None:
            break
        print(f"{name} consume: {item}")
    print(f"{name} consumer done")

q : Queue[int|None] = Queue()

p = threading.Thread(target=producer, args=(q,))
c1 = threading.Thread(target=consumer, args=("C1",q))
c2 = threading.Thread(target=consumer, args=("C2",q))

p.start()
c1.start()
c2.start()

p.join()
c1.join()
c2.join()
