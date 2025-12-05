import threading
import time
from fib import fib, N, FIB_N

results : list[int|None] = [None] * N

def worker(i: int) -> None:
    results[i] = fib(FIB_N)

threads : list[threading.Thread] = []
for i in range(N):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)

print("Start")
start = time.perf_counter()
for t in threads:
    t.start()
for t in threads:
    t.join()
end = time.perf_counter()
diff = end-start
print(f"Done in {diff:.6f} seconds")
