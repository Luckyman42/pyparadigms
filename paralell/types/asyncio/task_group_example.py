import asyncio
from typing import Coroutine, Any, Never

async def basic_double(n : int):
    double = n
    print(f"start - {n}")  
    await asyncio.sleep(n)
    print(f"double - {n}")  
    double += n
    await asyncio.sleep(n)
    print(f"end - {n}")  
    return double

async def wrong_double(n : int) -> Never:
    double = n
    print(f"start - {n}")  
    await asyncio.sleep(n)
    print(f"double - {n}")  
    double += n
    raise RuntimeError("Something went wrong")

async def one_worng():
    print("Creating the async tasks")
    try:
        async with asyncio.TaskGroup() as tg:
            t_good = tg.create_task(basic_double(10))
            t_wrong = tg.create_task(wrong_double(1))
            print("wait for it")
        print(f"Done! 1: {t_good.result()}, 2: {t_wrong.result()}")
    except ExceptionGroup as eg:
        print("Exception happend: ", eg.args)
        print("Good was cancalled: ", t_good.cancelled())
        print("wrong was cancalled: ", t_wrong.cancelled())
        
async def both_good():
    print("Creating the async tasks")
    try:
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(basic_double(3))
            t2 = tg.create_task(basic_double(2))
            print("wait for it")
        print(f"Done! 1: {t1.result()}, 2: {t2.result()}")
        print(f"Cancelled? 1: {t1.cancelled()}, 2: {t2.cancelled()}")
    except ExceptionGroup as eg:
        print("Exception happend: ", eg.args)

async def main_task(a: Coroutine[Any,Any, int],
               b: Coroutine[Any,Any, int]):
    print("Create tasks") 
    ta = asyncio.create_task(a)
    tb = asyncio.create_task(b)
    print("wait for it")
    ra = None
    rb = None
    try:
        await ta
        if ta.cancelled():
            print ("First was cancalled!")
        else:
            ra = ta.result()
    except RuntimeError:
        print("A task failed")
    try:
        await tb
        if tb.cancelled():
            print ("Second was cancalled!")
        else:
            rb = tb.result()
    except RuntimeError:
        print("B task failed")
 
    print(f"Both tasks have completed now: {ra}, {rb}")


if __name__ == "__main__":
    print("Lets se what the difference between running two tasks seperatly or in a TaskGroup")
    print("Run two task separatly")
    asyncio.run(main_task(basic_double(3),basic_double(2)))
    print("\nRunning them in taskGroup")
    asyncio.run(both_good())
    
    print("\n------------------------------\n")
    print("Lets se whats happend if one of the task are failed")
    print("Run two task separatly")
    asyncio.run(main_task(basic_double(10),wrong_double(1)))
    print("\nRunning them in taskGroup")
    asyncio.run(one_worng())
    print("As you can se, the difference is that if one of the tasks are failed the taskgroup will cancel the others")

