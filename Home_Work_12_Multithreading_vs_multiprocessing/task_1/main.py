import os.path
import threading
import requests
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

INPUT_IMG = "Input"

parent_folder = os.path.abspath(os.path.join(os.getcwd(), ".."))
new_folder = os.path.join(parent_folder, INPUT_IMG)

os.makedirs(new_folder, exist_ok=True)


def download_file(url: str, filename: str) -> None:
    """Downloads a file from a given URL.

    Args:
        url: The URL of the file to download.
        filename: The name of the file to save locally.

    Raises:
       requests.Timeout: If the request times out.
       requests.HTTPError: If an HTTP error occurs during the download.
       requests.RequestException: If any other error occurs during the download process.
    """

    filename_dir = os.path.join(new_folder, filename)

    if os.path.exists(filename_dir):
        logging.info(f"Файл {filename} уже существует, загрузки не будет.")
        return

    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        filename_dir = os.path.join(new_folder, filename)
        with open(filename_dir, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        logging.info(f"Файл {filename} успішно завантажено.")

    except requests.Timeout:
        logging.error(f"Таймаут во время загрузки {url}")
    except requests.HTTPError as err:
        logging.error(f"HTTP ошибка {err.response.status_code} при загрузке {url}")
    except requests.RequestException as err:
        logging.error(f"Ошибка во время загрузки {url}: {err}")


if __name__ == "__main__":
    urls = [
        (
            "https://cdn.pixabay.com/photo/2018/04/22/12/48/owl-3340957_1280.jpg",
            "file1.jpg",
        ),
        (
            "https://cdn.pixabay.com/photo/2021/12/21/08/29/owl-6884773_1280.jpg",
            "file2.jpg",
        ),
        (
            "https://cdn.pixabay.com/photo/2018/10/08/14/46/bird-3732867_1280.jpg",
            "file3.jpg",
        ),
    ]
    threads = []
    for url_download, filename_loaded in urls:
        thread = threading.Thread(
            target=download_file, args=(url_download, filename_loaded)
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("Все файлы загружены!")
