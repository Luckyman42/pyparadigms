import asyncio
from typing import Coroutine, Any
import time

async def async_loop(name: str, n : int):
    print(f"[{name}] start - loop({n})")
    for i in range(n):
        await asyncio.sleep(1)
        print(f"[{name}] {i}. iter - loop({n})")
    print(f"[{name}] end - loop({n})")

async def sync_loop(name: str, n : int):
    print(f"[{name}] start - loop({n})")
    for i in range(n):
        time.sleep(1)
        print(f"[{name}] {i}. iter - loop({n})")
    print(f"[{name}] end - loop({n})")


async def main(
        l1: Coroutine[Any,Any,None],
        l2: Coroutine[Any,Any,None],
        l3: Coroutine[Any,Any,None]):
    async with asyncio.TaskGroup() as tg:
        tg.create_task(l1)
        tg.create_task(l2)
        tg.create_task(l3)
        print("wait for them")
    print("Done!")


if __name__ == "__main__":
    print("Lets see if all using async block")
    asyncio.run(main(
        async_loop("A1",5),
        async_loop("A2",5),
        async_loop("A3",5),
    ))
    print("\n----------------\n")
    print("Lets see if one is using a sync block")
    asyncio.run(main(
        async_loop("A1",5),
        async_loop("A2",5),
        sync_loop("S",5),
    ))


