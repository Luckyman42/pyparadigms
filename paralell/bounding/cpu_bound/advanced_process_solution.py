import time
from fib import fib, N, FIB_N
from concurrent.futures import ProcessPoolExecutor, as_completed

W = 6


print("Start")
start = time.perf_counter()

with ProcessPoolExecutor(max_workers=W) as exe:
    futures = [exe.submit(fib, FIB_N) for _ in range(N)]
    results = [f.result() for f in as_completed(futures)]
    end = time.perf_counter()
    print(results)
    diff = end-start
    print(f"Done in {diff:.6f} seconds")
