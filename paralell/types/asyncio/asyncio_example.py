import asyncio
from typing import Coroutine, Any

async def stop(n : int):
    await asyncio.sleep(n)

async def thinking():
    await asyncio.sleep(1)
    return 42    

async def stop_twice(n : int):
    print(f"start - stop_twice({n})")
    await asyncio.sleep(n)
    print(f"middle - stop_twice({n})")
    await asyncio.sleep(n)
    print(f"end - stop_twice({n})")

async def async_loop(n : int):
    print(f"start - loop({n})")
    for i in range(n):
        await asyncio.sleep(1)
        print(f"{i}. iter - loop({n})")
    print(f"end - loop({n})")


async def main():
    print("start main")
    await stop(3)
    async_nothing : Coroutine[Any, Any, None] = stop(2)
    await async_nothing
    the_coro : Coroutine[Any, Any, int] = thinking()
    the_result = await the_coro
    print(f"The result is: {the_result}")

    print("Starting the async functions")
    astop = stop_twice(5)
    aloop = async_loop(10)
    print("waiting so the event loop will pass the process to other")
    await asyncio.sleep(6)
    print("wait for the stop_twice")
    await astop
    print("wait for the loop")
    await aloop
    print("as you can see the functions start only when we call an await on them")

if __name__ == "__main__":
    asyncio.run(main())

