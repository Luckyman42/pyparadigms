from multiprocessing import Process, set_start_method
from typing import Literal

def global_worker():
    print("global worker")

def main(method :Literal["fork","spawn"] = "fork", local : bool = True):
    set_start_method(method)

    def local_worker():
        print("local worker")

    p1 = Process(target=(local_worker if local else global_worker))
    p1.start()
    p1.join()



if __name__ == "__main__":
    print("main")
    main(method="fork", local=True)

# fork will get the memory of its parent
# spawn will initalize empty and get only the local 