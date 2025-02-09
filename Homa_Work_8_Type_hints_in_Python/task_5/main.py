from typing import Callable


def square(x: int) -> int:
    """Calculates the square of a number.
    This function takes an integer as input and returns its square.
    """
    return x**2


def double(x: int) -> int:
    """Doubles the input integer.
    This function takes an integer and returns its double.
    """
    return 2 * x


def apply_operation(x: int, operation: Callable[[int], int]) -> int:
    """Applies a given operation to an integer.
    This function takes an integer and a callable operation (a function that takes an integer and returns an integer), and applies the operation to the input integer.
    """
    return operation(x)


if __name__ == "__main__":
    print(apply_operation(5, square))  # 25
    print(apply_operation(5, double))  # 10
