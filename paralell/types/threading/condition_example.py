import threading
import time

def producer(li: list[int], cond : threading.Condition, is_end : threading.Event):
    for i in range(5):
        with cond:
            li.append(i)
            cond.notify()
        print(f"Produce: {i}")
        time.sleep(1)
    print("Producer done")
    with cond:
        cond.notify_all()
    is_end.set()

def consumer(name : str, li: list[int], cond : threading.Condition, is_end : threading.Event):
    while not is_end.is_set():
        print(f"{name} is waiting")
        with cond:
            cond.wait()
            if not li:
               break
            item = li.pop()
        print(f"{name} consume: {item}")
    print(f"{name} consumer done")



condition = threading.Condition()
shared : list[int] = []
end = threading.Event()

p = threading.Thread(target=producer, args=(shared,condition,end))
c1 = threading.Thread(target=consumer, args=("C1",shared,condition,end))
c2 = threading.Thread(target=consumer, args=("C2",shared,condition,end))

p.start()
c1.start()
c2.start()

p.join()
c1.join()
c2.join()
