import asyncio
import logging
import random


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def download_page(url: str) -> None:
    """Simulate downloading a web page.

    This coroutine simulates the process of downloading a web page by pausing for a random amount of time (between 1 and 5 seconds). It then logs a message indicating the completion of the download.

    Args:
        url (str): The URL of the page being downloaded (used only for logging).

    Returns:
        None
    """

    time_load = random.randint(1, 5)
    await asyncio.sleep(time_load)
    logging.info(f"Страница {url} загружена за {time_load} секунд")


async def main(urls: list) -> None:
    """Download multiple web pages concurrently.

    This coroutine takes a list of URLs and simulates downloading each page concurrently using asyncio.gather. It utilizes the download_page coroutine for each URL.

    Args:
        urls (list): A list of URLs to download.

    Returns:
        None
    """

    tasks = [download_page(url) for url in urls]
    await asyncio.gather(*tasks)


url_list = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]


asyncio.run(main(url_list))
