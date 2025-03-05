import asyncio
import logging
import aiohttp

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

semaphore = asyncio.Semaphore(3)


async def download_page(url: str) -> None:
    """Download a web page asynchronously.

    Args:
        url: The URL of the page to download.

    Returns:
        None

    Raises:
        aiohttp.ClientError: If there is a network error during the download.
        asyncio.TimeoutError: If the download times out.
    """

    async with semaphore:
        timeout = aiohttp.ClientTimeout(total=10)
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        await response.text()
                        logging.info(f"Страница {url} загружена.")
                    else:
                        logging.warning(f"Ошибка {response.status} при загрузке {url}")
        except asyncio.TimeoutError:
            logging.error(f"Тайм-аут при загрузке {url}")
        except aiohttp.ClientError as e:
            logging.error(f"Ошибка сети при загрузке {url}: {e}")


async def main(urls: list) -> None:
    """Download multiple web pages concurrently.

    This coroutine takes a list of URLs and simulates downloading each page concurrently using asyncio.gather. It utilizes the download_page coroutine for each URL.

    Args:
        urls (list): A list of URLs to download.

    Returns:
        None
    """
    logging.info("Загрузка страниц...")
    await asyncio.gather(*[download_page(url) for url in urls])
    logging.info("Загрузка завершена.")


url_list = [
    "https://ru.wikipedia.org/wiki/Хопкинс,_",
    "https://ru.wikipedia.org/wiki/Хопкинс,_Энтони",
    "https://ru.wikipedia.org/wiki/Молчание_ягнят_(роман)",
    "https://ru.wikipedia.org/wiki/Актёрское_искусство",
]


asyncio.run(main(url_list))
