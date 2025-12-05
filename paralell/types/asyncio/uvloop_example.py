import uvloop
import asyncio

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Now the asyncio event loop run in C, not Python
