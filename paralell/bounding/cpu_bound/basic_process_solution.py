from multiprocessing import Process, Manager
import time
from fib import fib, N, FIB_N

def worker(i: int, shared: list) -> None:
    shared[i] = fib(FIB_N)


if __name__ == '__main__':
    manager = Manager()
    shared = manager.list([None] * N)
    procs : list[Process] = []
    for i in range(N):
        p = Process(target=worker, args=(i, shared))
        procs.append(p)

    print("Start")
    start = time.perf_counter()
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print(list(shared))
    end = time.perf_counter()
    diff = end-start
    print(f"Done in {diff:.6f} seconds")
