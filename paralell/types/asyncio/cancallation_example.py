import asyncio
from asyncio_example import stop_twice, async_loop

async def cancellable_stop_twice(n : int):
    try:
        await stop_twice(n)
    except asyncio.CancelledError:
        print("CancalledError! - stop_twice")
    finally:
        print("Finally - stop_twice")

async def cancellable_async_loop(n : int):
    try:
        await async_loop(n)
    except asyncio.CancelledError:
        print("CancalledError! - loop")
    finally:
        print("Finally - loop ")



async def main():
    print("Creating the async tasks")
    astop = asyncio.create_task(cancellable_stop_twice(5))
    aloop = asyncio.create_task(cancellable_async_loop(10))
    print("waiting so the event loop will pass the process to other")
    await asyncio.sleep(6)
    print("cancel stop_twice")
    astop.cancel()
    print("wait for the stop_twice")
    await astop
    print("wait for the loop")
    await aloop
    print("as you can see after the cancellation the process get an exception but it doesn't effect the other task")


if __name__ == "__main__":
    asyncio.run(main())

