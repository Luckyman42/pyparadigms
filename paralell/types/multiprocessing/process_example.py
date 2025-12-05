from multiprocessing import Process
import time

def worker(name : str):
    print(f"{name} start")
    time.sleep(1)
    print(f"{name} end")

p1 = Process(target=worker, args=("P1",))
p2 = Process(target=worker, args=("P2",))

p1.start()
p2.start()

p1.join()
p2.join()
