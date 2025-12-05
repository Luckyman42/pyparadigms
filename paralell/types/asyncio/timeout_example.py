import asyncio
from typing import Callable, Coroutine, Any
from cancallation_example import cancellable_stop_twice
from asyncio_example import stop_twice


async def main(f: Callable[[int],Coroutine[Any,Any, None]]):
    print("Creating the async tasks")
    astop = asyncio.create_task(f(100))
    print("waiting so the event loop will pass the process")
    await asyncio.sleep(3)
    print("wait with little timout on the task")
    try:
        await asyncio.wait_for(astop, timeout=2.0)
        print("successfully waited")
    except asyncio.TimeoutError:
        print("Timeout happend")


async def sleep_after_cancell(n : int):
    try:
        await stop_twice(n)
    except asyncio.CancelledError:
        print("CancalledError! - stop_twice")
    finally:
        await asyncio.sleep(5)
        print("Finally - stop_twice")


if __name__ == "__main__":
    asyncio.run(main(stop_twice))
    print("")
    print("Now try the same thing but with CancelledError handling in the task")
    asyncio.run(main(cancellable_stop_twice))
    print("")
    print("Now try the same thing but sleep after handling CancelledError")
    asyncio.run(main(sleep_after_cancell))
    print("The last two times is the same becuase the wait_for cancelled the task if runs out of time")


