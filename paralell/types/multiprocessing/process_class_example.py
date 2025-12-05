from multiprocessing import Process
import time

class MyProcess(Process):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def run(self):
        print(f"Process {self.name} start")
        time.sleep(1)
        print(f"Process {self.name} end")

p1 = MyProcess("P1")
p2 = MyProcess("P2")

p1.start()
p2.start()
p1.join()
p2.join()
