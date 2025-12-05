from typing import Any
from multiprocessing import Process, Value, Lock

def worker(counter : Any, lock: Any):
    for _ in range(10000):
        with lock:
            counter.value += 1

lock = Lock()
counter = Value('i', 0)
p1 = Process(target=worker, args=(counter,lock))
p2 = Process(target=worker, args=(counter,lock))

p1.start(); p2.start()
p1.join(); p2.join()

print(counter.value)


print("\n--------n")


def worker2(counter : Any):
    for _ in range(10000):
        with counter.get_lock():
            counter.value += 1

counter2 = Value('i', 0)

p1 = Process(target=worker2, args=(counter2,))
p2 = Process(target=worker2, args=(counter2,))

p1.start(); p2.start()
p1.join(); p2.join()

print(counter2.value)
