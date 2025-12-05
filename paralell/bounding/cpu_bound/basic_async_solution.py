import asyncio
import time
from fib import fib, N, FIB_N

async def worker(i: int) -> int:
    return fib(FIB_N)

async def main() -> None:
    tasks = [asyncio.create_task(worker(i)) for i in range(N)]
    results = await asyncio.gather(*tasks)
    print(results)

print("Start")
start = time.perf_counter()
asyncio.run(main())
end = time.perf_counter()
diff = end-start
print(f"Done in {diff:.6f} seconds")
