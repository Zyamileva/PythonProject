import logging
import aiohttp
import asyncio

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


MAX_CONCURRENT_REQUESTS = 3
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


async def fetch_content(url: str, session: aiohttp.ClientSession) -> str:
    """Fetch content from a URL using a given aiohttp session.

    Args:
        url: The URL to fetch content from.
        session: The aiohttp ClientSession to use for the request.

    Returns:
        The fetched content (truncated to 500 characters), or an error message if the request fails.
    """

    async with semaphore:
        timeout = aiohttp.ClientTimeout(total=10)
        try:
            async with session.get(url, timeout=timeout) as response:
                if response.status != 200:
                    return f"Ошибка {response.status} при загрузке {url}"
                content = await response.text()
                return content[:500]
        except asyncio.TimeoutError:
            return f"Тайм-аут для {url}"
        except aiohttp.ClientError as e:
            return f"Ошибка сети {url}: {str(e)}"


async def fetch_all(urls: list) -> list:
    """Fetch content from multiple URLs concurrently.

    Args:
        urls: A list of URLs to fetch content from.

    Returns:
        A list of fetched content, corresponding to the order of URLs in the input list.
    """

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_content(url, session) for url in urls]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":
    urls = [
        "https://engoo.com",
        "https://zyamileva.github.io/CodeForFood/",
        "https://www.wikipedia.org",
    ]

    results = asyncio.run(fetch_all(urls))

    for content in results:
        logging.info(f"Содержание сайта - {content}\n")
