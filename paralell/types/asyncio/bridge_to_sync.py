from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import asyncio
import time

# Run in different Process
# Optimal for CPU bound tasks

print("Running in ProcessPool:")

def heavy(x: int):
    return sum(i*i for i in range(x))

async def main_process():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, heavy, 10_000_000)
        print(result)

asyncio.run(main_process())


# Run in a different Thread
# Optimal if the code doesn't support async functions (like oracle)

print("Running in ThreadPool:")

def blocking_io():
    time.sleep(3)
    return "done"

async def main_thread():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_io)
        print(result)

asyncio.run(main_thread())

print("Syntax sugar for sending into a thread: ")
# There is a shorter syntax for send the task to a thread

async def main():
    result = await asyncio.to_thread(blocking_io)
    print(result)

asyncio.run(main())