def parse_input(number: int | str) -> int | None:
    """Parses an input value and attempts to convert it to an integer.
    This function takes a number as input, which can be either an integer or a string. It attempts to convert the input to an integer and returns the integer if successful. If the input cannot be converted, it returns None.
    """
    try:
        return int(number) if int(number).is_integer() else None
    except ValueError:
        return None


if __name__ == "__main__":
    print(parse_input(42))  # 42
    print(parse_input("100"))  # 100
    print(parse_input("hello"))  # None
