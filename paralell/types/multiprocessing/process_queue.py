import multiprocessing as mp
import time

def producer(q: mp.Queue):
    for i in range(5):
        q.put(i)
        print("Producer:", i)
        time.sleep(0.5)
    q.put(None) 

def consumer(q: mp.Queue):
    while True:
        item = q.get()
        if item is None:
            break
        print("Consumer:", item)

q: mp.Queue = mp.Queue()

p = mp.Process(target=producer, args=(q,))
c = mp.Process(target=consumer, args=(q,))

p.start(); c.start()
p.join(); c.join()
