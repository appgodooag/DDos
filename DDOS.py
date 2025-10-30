import asyncio
import aiohttp
import time

URL = ""
CONCURRENCY = 10  
REQUESTS = 1000000000000000  
DELAY = 0

sem = asyncio.Semaphore(CONCURRENCY)

async def fetch(session, i):
    async with sem:
        try:
            async with session.get(URL, timeout=10) as resp:
                text = await resp.text()
                return resp.status
        except Exception as e:
            return f"ERR: {e}"

async def worker(name, session, n):
    
    for i in range(n):
        status = await fetch(session, i)
        print(f"worker {name} -> {status}")
        await asyncio.sleep(DELAY)

async def main():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        workers = [worker(i, session, REQUESTS//CONCURRENCY) for i in range(CONCURRENCY)]
        await asyncio.gather(*workers)
    print("done in", time.time() - start)

if __name__ == "__main__":
    asyncio.run(main())