def is_even(n: int) -> bool:
    """
    Checks if a number is even.

     >>> is_even(2)
     True
     >>> is_even(3)
     False
     >>> is_even(0)
     True
     >>> is_even(-1)
     False
    """
    return n % 2 == 0


def factorial(n: int) -> int:
    """
    Calculates the factorial of a number.

    >>> factorial(0)
    1
    >>> factorial(1)
    1
    >>> factorial(7)
    5040
    >>> factorial(10)
    3628800
    """
    if n < 0:
        raise ValueError("Factorial is defined only for non-negative numbers")
    return 1 if n == 0 else n * factorial(n - 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
