from typing import List, Tuple


def filter_adults(people: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    """Filters a list of people to include only adults.
    This function takes a list of tuples, where each tuple contains a person's name and age, and returns a new list containing only the tuples representing adults (age 18 or older).
    """
    return [person for person in people if person[1] >= 18]


if __name__ == "__main__":
    people = [("Андрій", 25), ("Олег", 16), ("Марія", 19), ("Ірина", 15)]
    print(filter_adults(people))
