import multiprocessing
import numpy as np


def sum_part(num):
    """Calculates the sum of elements in an iterable.

    Args:
        num: An iterable of numbers.

    Returns:
        The sum of the numbers in the input iterable.
    """
    return sum(num)


def parallel_sum(numbers, num_processes):
    """Calculates the sum of a list of numbers in parallel.

    Args:
        numbers: A list of numbers to sum.
        num_processes: The number of processes to use for parallel computation.

    Returns:
        The sum of all numbers in the input list.
    """

    chunk_size = len(numbers) // num_processes

    chunks = [
        numbers[i * chunk_size : (i + 1) * chunk_size] for i in range(num_processes - 1)
    ] + [numbers[(num_processes - 1) * chunk_size :]]

    with multiprocessing.Pool(processes=num_processes) as pool:
        partial_sums = pool.map(sum_part, chunks)

    return sum(partial_sums)


if __name__ == "__main__":
    list_int = np.random.randint(1, 100, size=1000000).tolist()

    num_processes = multiprocessing.cpu_count()

    total_sum = parallel_sum(list_int, num_processes)

    print(f"Общая сумма: {total_sum}")
