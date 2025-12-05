import asyncio
from asyncio_example import stop,thinking, stop_twice, async_loop

async def main():
    print("start main")
    # task <: future <: awaitable
    await stop(3)
    async_nothing : asyncio.Task[None] = asyncio.create_task(stop(2))
    await async_nothing
    the_task :  asyncio.Task[int]  = asyncio.create_task(thinking())
    the_result = await the_task
    print(f"The result is: {the_result}")

    print("Creating the async tasks")
    astop = asyncio.create_task(stop_twice(5))
    aloop = asyncio.create_task(async_loop(10))
    print("waiting so the event loop will pass the process to other")
    await asyncio.sleep(6)
    print("wait for the stop_twice")
    await astop
    print("wait for the loop")
    await aloop
    print("as you can see the functions start after the task is created just not getting the process until the first await")

if __name__ == "__main__":
    asyncio.run(main())
