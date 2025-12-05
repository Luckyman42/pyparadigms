import asyncio
from concurrent.futures import ProcessPoolExecutor
import time
from fib import fib, N, FIB_N

W = 6

async def worker(i: int) -> int:
    return fib(FIB_N)

async def main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor(max_workers=W) as exe:
        tasks = [loop.run_in_executor(exe, fib, FIB_N) for _ in range(N)]
        results = await asyncio.gather(*tasks)
        print(results)

print("Start")
start = time.perf_counter()
asyncio.run(main())
end = time.perf_counter()
diff = end-start
print(f"Done in {diff:.6f} seconds")
