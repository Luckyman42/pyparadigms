import threading
from queue import Queue
import time

def producer(q : Queue[int|None]):
    for i in range(5):
        q.put(i)
        print(f"Produce: {i}")
        time.sleep(1)
    q.put(None)  # jelzés a consumernek

def consumer(q: Queue[int|None]):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"Consume: {item}")

q : Queue[int|None] = Queue()

t1 = threading.Thread(target=producer, args=(q,))
t2 = threading.Thread(target=consumer, args=(q,))

t1.start()
t2.start()

t1.join()
t2.join()
