def divide(a: int, b: int) -> float:
    """
    This function divides two integers and returns the result as a float.
    >>>divide(14,2)
    7.0
    >>> divide(8,4)
    2.0
    >>> divide(5,0)
     Traceback (most recent call last):
        ...
    ZeroDivisionError: Division by zero is impossible
    """
    if b == 0:
        raise ZeroDivisionError("Division by zero is impossible")
    return a / b

if __name__ == "__main__":
    print(divide(5,1))
