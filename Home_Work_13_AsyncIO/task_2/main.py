import logging

import aiohttp
import asyncio


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def fetch_content(url: str) -> str:
    """Fetch content from a given URL.

    This coroutine retrieves the content from the specified URL using aiohttp. It handles potential connection errors and timeouts.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The content of the URL as a string, or an error message if the request fails.
    """

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.client_exceptions.ClientConnectorDNSError as e:
        return f"Ошибка запроса {url}: {str(e)}"
    except asyncio.TimeoutError:
        return f"Время ожидания для {url} исчерпано."


async def fetch_all(urls: list) -> list:
    """Fetch content from multiple URLs concurrently.

    This coroutine fetches content from a list of URLs using asyncio.gather for concurrent execution. It returns a list of results, where each result corresponds to the content or error message from each URL.

    Args:
        urls (list): A list of URLs to fetch content from.

    Returns:
        list: A list of strings, where each string is either the fetched content or an error message.
    """

    tasks = [fetch_content(url) for url in urls]
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    urls = [
        "https://engoo.com",
        "https://zyamileva.github.io/CodeForFood/",
        "https://www.wikipedia.org",
    ]

    results = asyncio.run(fetch_all(urls))

    for content in results:
        logging.info(f"Содержание сайта - {content[:300]}\n")
