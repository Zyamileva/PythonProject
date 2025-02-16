import re


def data_format(text: str) -> str:
    """Reformats dates from DD/MM/YYYY to YYYY-MM-DD format.

    This function uses a regular expression to find and replace dates in the input string.

    Args:
        text: The input string containing dates in DD/MM/YYYY format.

    Returns:
        The input string with dates reformatted to YYYY-MM-DD.
    """
    pattern_data = r"(\d{2})/(\d{2})/(\d{4})"
    return re.sub(pattern_data, r"\3-\2-\1", text)


print(data_format("01/02/2000"))
