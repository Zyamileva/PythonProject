import requests
import aiohttp
import asyncio
import time
import threading
import multiprocessing

URL = "https://zyamileva.github.io/CodeForFood/"
COUNT = 500


# Синхроный подход
def synchronous_requests():
    start_time = time.time()
    for _ in range(COUNT):
        requests.get(URL)
    print(f"Синхронный подход: {time.time() - start_time:.2f} сек")


# Многопоточный подход
def multithreaded_requests():
    start_time = time.time()

    def fetch():
        requests.get(URL)

    threads = [threading.Thread(target=fetch) for _ in range(COUNT)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print(f"Многопоточный: {time.time() - start_time:.2f} сек")


# Многопроцесорный подход
def fetch(_):
    requests.get(URL)


def process_requests():
    start_time = time.time()

    with multiprocessing.Pool(processes=8) as pool:
        pool.map(fetch, range(COUNT))

    print(f"Многопроцессорный: {time.time() - start_time:.2f} сек")


# Асинхронный подход
async def async_requests():
    start_time = time.time()

    async def fetch(session):
        async with session.get(URL) as response:
            return await response.text()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session) for _ in range(COUNT)]
        await asyncio.gather(*tasks)

    print(f"Асинхронный: {time.time() - start_time:.2f} сек")


if __name__ == "__main__":
    print("\n Старт...")

    synchronous_requests()
    multithreaded_requests()
    process_requests()
    asyncio.run(async_requests())
