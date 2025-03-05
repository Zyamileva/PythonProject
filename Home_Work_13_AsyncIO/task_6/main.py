import logging

import aiohttp
import asyncio


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


semaphore = asyncio.Semaphore(5)


async def download_image(url: str, filename: str) -> None:
    """Download an image from a URL.

    Args:
        url: The URL of the image to download.
        filename: The name of the file to save the image to.

    Returns:
        None
    """

    try:
        async with aiohttp.ClientSession() as session:
            async with semaphore, session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    with open(filename, "wb") as file:
                        file.write(image_data)
                    logging.info("Изображение загружено.")
                else:
                    logging.error(f"Ошибка {response.status} для {url}")
    except asyncio.TimeoutError:
        logging.error(f"Время ожидания истекло для {url}")
    except aiohttp.ClientError as e:
        logging.error(f"Ошибка клиента при загрузке {url}: {e}")
    except Exception as e:
        logging.error(f"Неизвестная ошибка при загрузке {url}: {e}")


async def main(urls: dict) -> None:
    """Download multiple images concurrently.

    Args:
        urls: A dictionary mapping image URLs to filenames.

    Returns:
        None
    """

    tasks = [download_image(url, filename) for url, filename in urls.items()]
    await asyncio.gather(*tasks)


image_urls = {
    "https://cdn.pixabay.com/photo/2018/04/22/12/48/owl-3340957_1280.jpg": "image1.jpg",
    "https://cdn.pixabay.com/photo/2021/12/21/08/29/owl-6884773_1280.jpg": "image2.jpg",
    "https://cdn.pixabay.com/photo/2018/10/08/14/46/bird-3732867_1280.jpg": "image3.jpg",
}

asyncio.run(main(image_urls))
