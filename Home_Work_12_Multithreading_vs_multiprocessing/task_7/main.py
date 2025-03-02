import math
import multiprocessing
import concurrent.futures


def partial_factorial(start, end):
    """Calculates the factorial of a range of numbers.

    Args:
        start: The starting integer of the range (inclusive).
        end: The ending integer of the range (inclusive).

    Returns:
        The product of all integers from start to end.
    """

    result = 1
    for i in range(start, end + 1):
        result *= i
    return result


def wrapper_partial_factorial(range_tuple):
    """Wrapper function for partial_factorial.

    Args:
        range_tuple: A tuple containing the start and end of the range for factorial calculation.

    Returns:
        The result of the partial_factorial calculation.
    """

    return partial_factorial(*range_tuple)


def parallel_factorial(number, num_processes):
    """Calculates the factorial of a number using parallel processing.

    Args:
        number: The number for which to calculate the factorial.
        num_processes: The number of processes to use.

    Returns:
        The factorial of the input number.
    """

    if number in [0, 1]:
        return 1

    step = number // num_processes
    ranges = [(i * step + 1, min((i + 1) * step, number)) for i in range(num_processes)]
    if ranges[-1][1] < number:
        ranges[-1] = (ranges[-1][0], number)

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        partial_results = list(executor.map(wrapper_partial_factorial, ranges))

    return math.prod(partial_results)


if __name__ == "__main__":
    num_processes = multiprocessing.cpu_count()

    n = int(input("Enter a number: "))

    result = parallel_factorial(n, num_processes)

    print(f"Факториал числа {n}! вычислен. Результат равен: {result}")
