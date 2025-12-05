from threading import Thread
import time

def worker(name :str):
    print(f"{name} start")
    time.sleep(1)
    print(f"{name} end")

t1 = Thread(target=worker, args=("T1",))
t2 = Thread(target=worker, args=("T2",))

t1.start()
t2.start()

t1.join()
t2.join()

