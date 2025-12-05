import asyncio

async def set_value[T](fut: asyncio.Future[T], delay: float, value : T ) -> None:
    print("Start setting value")
    await asyncio.sleep(delay)
    print("Value is set")
    fut.set_result(value)
    await asyncio.sleep(delay)
    print("End setting value")


async def main():
    print("Start main")
    # Get the current event loop
    loop = asyncio.get_running_loop()

    print("Create future")
    # Create new Future object
    fut = loop.create_future()
    print("Create Task")
    loop.create_task(set_value(fut,1,"Hello"))

    print("Wait for value")
    # The await wait until the future object has its value not for the function end
    value = await fut
    print("Get the value")
    print("Value: ",value)
    print("End main")

asyncio.run(main())

