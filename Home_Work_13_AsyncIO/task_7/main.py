import requests
import aiohttp
import asyncio
import time
import threading
import multiprocessing
import logging


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)

URL = "https://zyamileva.github.io/CodeForFood/"
COUNT = 500


# Синхроный подход
def synchronous_requests():
    """Make synchronous requests to a URL.

    Returns:
        None
    """
    start_time = time.time()
    for _ in range(COUNT):
        try:
            response = requests.get(URL, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.info(f"Ошибка при запросе:{e}")
    logging.info(f"Синхронный подход: {time.time() - start_time:.2f} сек")


# Многопоточный подход
def multithreaded_requests():
    """Make multithreaded requests to a URL.

    Returns:
        None
    """
    start_time = time.time()

    def fetch():
        """Fetch content from a URL.

        Returns:
            None
        """
        try:
            response = requests.get(URL, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Ошибка при запросе {e}")

    threads = [threading.Thread(target=fetch) for _ in range(COUNT)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    logging.info(f"Многопоточный: {time.time() - start_time:.2f} сек")


# Многопроцесорный подход
def fetch(_):
    """Fetch data from a URL.

    Args:
        _: Unused argument.

    Returns:
        None
    """
    try:
        responce = requests.get(URL)
        responce.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе:{e}")


def process_requests():
    """Process multiple requests using multiprocessing.

    Returns:
        None
    """
    start_time = time.time()

    with multiprocessing.Pool(processes=8) as pool:
        pool.map(fetch, range(COUNT))

    logging.info(f"Многопроцессорный: {time.time() - start_time:.2f} сек")


# Асинхронный подход
async def async_requests():
    start_time = time.time()

    async def fetch(session):
        """Make asynchronous requests to a URL.

        Returns:
            None
        """
        try:
            async with session.get(URL, timeout=5) as response:
                response.raise_for_status()
                return await response.text()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logging.error(f"Ошибка при запросе: {e}")
            return None

    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(20)

        async def sem_fetch():
            async with semaphore:
                return await fetch(session)

        tasks = [sem_fetch() for _ in range(COUNT)]
        await asyncio.gather(*tasks)

    logging.info(f"Асинхронный: {time.time() - start_time:.2f} сек")


if __name__ == "__main__":
    logging.info("\n Старт...")

    synchronous_requests()
    multithreaded_requests()
    process_requests()
    asyncio.run(async_requests())
