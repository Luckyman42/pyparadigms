import asyncio
import aiohttp
import time
URL = "https://google.com"
N = 100

async def fetch(session : aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as resp:
        return await resp.text()

async def main() -> list[str]:
    tasks : list[asyncio.Task[str]] = []
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            for _ in range(N):
                t = tg.create_task(fetch(session, URL))
                tasks.append(t)
    return [task.result() for task in tasks]

print(f"Start {N} request")
start = time.perf_counter()
results = asyncio.run(main())
end = time.perf_counter()
diff = end-start
print(f"Done with: {len(results)} in {diff:.6f} seconds")
