import logging

import aiohttp
import asyncio


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def download_image(url: str, filename: str) -> None:
    """Download an image from a given URL.

    This function asynchronously downloads an image from the specified URL and saves it to the given filename.
    It uses aiohttp to make the request and handles potential errors during download.

    Args:
        url (str): The URL of the image to download.
        filename (str): The name of the file to save the image to.

    Returns:
        None
    """

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    with open(filename, "wb") as file:
                        file.write(image_data)
                    logging.info("Изображение загружено.")
                else:
                    logging.info(f"Ошибка {response.status} для {url}")
    except Exception as e:
        logging.info(f"Ошибка при загрузке {url}: {e}")


async def main(urls: dict) -> None:
    """Download images from URLs concurrently.

    This function takes a dictionary of URLs and filenames and downloads the images concurrently using asyncio.gather.
    It creates a list of tasks using download_image coroutine for each URL-filename pair and awaits their completion.

    Args:
        urls (dict): A dictionary where keys are image URLs and values are corresponding filenames.

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
