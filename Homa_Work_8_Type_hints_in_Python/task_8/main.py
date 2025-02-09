from typing import TypeVar, List, Callable, Generic

T = TypeVar("T")


def double(x: int) -> int:
    """Doubles the input integer.
    This function takes an integer and returns its double.
    """
    return x * 2


def to_upper(s: str) -> str:
    """Converts a string to uppercase.
    This function takes a string and returns its uppercase version.
    """
    return s.upper()


class Processor(Generic[T]):
    """A class for processing lists of data.
    This class stores a list of data and provides a method to apply a function to each element.
    """

    def __init__(self, data: List[T]):
        self.data = data

    def apply(self, func: Callable[[T], T]) -> List[T]:
        return [func(item) for item in self.data]


if __name__ == "__main__":
    p1 = Processor([1, 2, 3])
    print(p1.apply(double))  # [2, 4, 6]

    p2 = Processor(["hello", "world"])
    print(p2.apply(to_upper))  # ["HELLO", "WORLD"]
