import logging
import multiprocessing
import random


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def sum_part(num: list) -> int:
    """Calculates the sum of elements in an iterable.

    Args:
        num: An iterable of numbers.

    Returns:
        The sum of the numbers in the input iterable.
    """
    return sum(num)


def parallel_sum(numbers: list, num_processes: int) -> int:
    """Calculates the sum of a list of numbers in parallel.

    Args:
        numbers: A list of numbers to sum.
        num_processes: The number of processes to use for parallel computation.

    Returns:
        The sum of all numbers in the input list.
    """
    if num_processes < 1:
        raise ValueError("Количество процессов должно быть >= 1")

    chunk_size = len(numbers) // num_processes

    chunks = [
        numbers[i * chunk_size : (i + 1) * chunk_size] for i in range(num_processes - 1)
    ] + [numbers[(num_processes - 1) * chunk_size :]]

    with multiprocessing.Pool(processes=num_processes) as pool:
        partial_sums = pool.map(sum_part, chunks)

    return sum(partial_sums)


if __name__ == "__main__":
    list_int = [random.randint(1, 100) for _ in range(1_000_000)]
    num_processes = min(multiprocessing.cpu_count(), len(list_int))

    total_sum = parallel_sum(list_int, num_processes)

    logging.info(f"Общая сумма: {total_sum}")
