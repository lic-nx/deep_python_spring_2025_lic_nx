import time
import argparse
import asyncio
import aiohttp


# pylint: disable=W0718
async def fetch_url(session, url, timeout=10):
    try:
        async with session.get(url.strip(), timeout=timeout) as resp:
            return await resp.text()
    except asyncio.TimeoutError:
        return {"error": "Время ожидания истекло"}
    except Exception as e:
        return {"error": f"Неизвестная ошибка: {e}"}


# pylint: disable=W0718
async def fetch_worker(session, que, name):
    print(f"fetch_worker {name} started")
    while True:
        url = await que.get()
        if url is None:
            break
        try:
            result = await fetch_url(session, url)
            print(f"Fetched {url}: {len(result)} bytes")
        except Exception as err:
            print(f"Error fetching {url}: {err}")
        finally:
            que.task_done()
    print(f"fetch_worker {name} finished")


async def run(args):
    t1 = time.time()
    que = asyncio.Queue()
    with open(args.urls_file, encoding='utf-8') as f:
        for url in f:
            await que.put(url.strip())
    async with aiohttp.ClientSession() as session:
        workers = [
            asyncio.create_task(
                fetch_worker(session, que, f"worker_{i}")
            )
            for i in range(args.concurrency)
        ]
        await que.join()
        for worker in workers:
            worker.cancel()
        await asyncio.gather(*workers, return_exceptions=True)
    t2 = time.time()
    print(f"Batch time: {t2 - t1:.2f} seconds")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch URLs concurrently.')
    parser.add_argument('-c',
                        '--concurrency',
                        type=int,
                        help='Number of concurrent requests')
    parser.add_argument('urls_file', type=str, help='File containing URLs')
    params = parser.parse_args()
    asyncio.run(run(params))
