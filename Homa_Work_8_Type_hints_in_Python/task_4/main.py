from typing import List, TypeVar

T = TypeVar("T")


def get_first(list_of_elements: List[T]) -> T | None:
    """Retrieves the first element of a list.
    This function takes a list and returns its first element. If the list is empty, it returns None.
    """
    return list_of_elements[0] if list_of_elements else None


if __name__ == "__main__":
    print(get_first([1, 2, 3]))  # 1
    print(get_first(["a", "b", "c"]))  # "a"
    print(get_first([]))  # None
