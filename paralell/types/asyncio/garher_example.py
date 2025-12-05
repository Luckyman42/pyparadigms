import asyncio
from typing import Coroutine, Any

async def aloop(name: str, n : int):
    print(f"[{name}] start - loop({n})")
    for i in range(n):
        await asyncio.sleep(1)
        print(f"[{name}] {i}. iter - loop({n})")
    print(f"[{name}] end - loop({n})")


async def number() -> int:
    return 42

async def nothing() -> None:
    await asyncio.sleep(1)

async def word() -> str:
    return "Hello World"

async def main(
        l1: Coroutine[Any,Any,Any],
        l2: Coroutine[Any,Any,Any],
        l3: Coroutine[Any,Any,Any]):
    print("wait for them")
    r = await asyncio.gather( l1, l2, l3 )
    print("Done!")
    print(r)

if __name__ == "__main__":
    asyncio.run(main(
        aloop("A1",2),
        aloop("A2",2),
        aloop("A3",2),
    ))
    asyncio.run(main(
        number(), nothing(), word()
    ))
