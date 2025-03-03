import concurrent.futures
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def search_in_file(filename: str, search_text: str) -> list:
    """Searches for a specific text within a file.

    Args:
        filename: The path to the file to search in.
        search_text: The text to search for.

    Returns:
        A list of tuples, where each tuple contains the filename, line number, and the line itself for each match. Returns an empty list if the file does not exist or if no matches are found.
    """

    results = []

    try:
        with open(filename, "r", encoding="utf-8", errors="ignore") as file:
            results.extend(
                (filename, line_num, line.strip())
                for line_num, line in enumerate(file, start=1)
                if search_text in line
            )
    except Exception as e:
        print(f"Ошибка при обработке {filename}: {e}")
    return results


def parallel_search(files: str, search_text: str, use_threads=True):
    """Performs a parallel search for a given text across multiple files.

    Args:
        files: A list of file paths to search within.
        search_text: The text to search for in each file.
        use_threads: If True, uses multithreading; otherwise, uses multiprocessing. Defaults to True.

    Returns:
        A list of tuples, where each tuple contains the filename, line number, and line content for each match found across all files.
    """

    executor_class = (
        concurrent.futures.ThreadPoolExecutor
        if use_threads
        else concurrent.futures.ProcessPoolExecutor
    )

    results = []
    with executor_class() as executor:
        future_to_file = {
            executor.submit(search_in_file, file, search_text): file for file in files
        }

        for future in concurrent.futures.as_completed(future_to_file):
            try:
                results.extend(future.result())
            except Exception as e:
                print(f"Ошибка: {e}")

    return results


if __name__ == "__main__":
    files_to_search = [
        "text1.txt",
        "text2.txt",
        "text3.txt",
    ]
    search_query = "Hello"

    # Многопоточность  (use_threads=True) или многопроцесорность (use_threads=False)
    results = parallel_search(files_to_search, search_query, use_threads=False)

    for filename, line_num, line in results:
        logging.info(f"Найдено в {filename}, ряд {line_num}: {line}")
