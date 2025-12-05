from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from fib import fib, N, FIB_N

W=6

print("Start")
start = time.perf_counter()
with ThreadPoolExecutor(max_workers=N) as exe:
    futures = [exe.submit(fib, FIB_N) for _ in range(N)]
    results = [f.result() for f in as_completed(futures)]
end = time.perf_counter()
print(results)
diff = end-start
print(f"Done in {diff:.6f} seconds")
