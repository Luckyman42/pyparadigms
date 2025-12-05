from threading import Thread
import time

class MyThread(Thread):
    def __init__(self, name : str):
        super().__init__()
        self.name = name

    def run(self):
        print(f"{self.name} start")
        time.sleep(1)
        print(f"{self.name} end")

t1 = MyThread("T1")
t2 = MyThread("T2")

t1.start()
t2.start()

t1.join()
t2.join()
