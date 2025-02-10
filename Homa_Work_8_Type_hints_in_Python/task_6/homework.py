from typing import List, Tuple, TypeVar, Callable

T = TypeVar("T")


def calculate_discount(price: float, discount: float) -> float:
    """Calculates the discounted price.
    This function takes an original price and a discount percentage, and returns the price after the discount is applied. Discounts greater than 100% result in a price of 0.
    """
    return 0.0 if discount > 100 else price - price * (discount / 100)


def filter_adults(people: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    """Filters a list of people to include only adults.
    This function takes a list of tuples, where each tuple contains a person's name and age, and returns a new list containing only the tuples representing adults (age 18 or older).
    """
    return [person for person in people if person[1] >= 18]


def parse_input(number: int | str) -> int | None:
    """Parses an input value and attempts to convert it to an integer.
    This function takes a number as input, which can be either an integer or a string. It attempts to convert the input to an integer and returns the integer if successful. If the input cannot be converted, it returns None.
    """
    try:
        return int(number) if int(number).is_integer() else None
    except ValueError:
        return None


def get_first(list_of_elements: List[T]) -> T | None:
    """Retrieves the first element of a list.
    This function takes a list and returns its first element. If the list is empty, it returns None.
    """
    return list_of_elements[0] if list_of_elements else None


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
    print(calculate_discount(100, 20))
    print(calculate_discount(50, 110))

    people = [("Андрій", 25), ("Олег", 16), ("Марія", 19), ("Ірина", 15)]
    print(filter_adults(people))

    print(parse_input(42))  # 42
    print(parse_input("100"))  # 100
    print(parse_input("hello"))  # None

    print(get_first([1, 2, 3]))  # 1
    print(get_first(["a", "b", "c"]))  # "a"
    print(get_first([]))  # None

    print(apply_operation(5, square))  # 25
    print(apply_operation(5, double))  # 10
