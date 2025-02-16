import re


def number_phone(text: str) -> str | None:
    """Attempts to extract a phone number from a given text.
    This function uses a regular expression to search for a phone number pattern in the input text.

    Args:
        text: The input string to search for a phone number.

    Returns:
        A match object if a phone number is found, otherwise None.
    """
    regular_phone = re.compile(r"\(?\d{3}\)?[ .-]?\d{3}[ -.]?\d{4}")
    return regular_phone.match(text)


phones = ("(123) 456-7890", "123-456-7890", "123.456.7890", "1234567890")
for phone in phones:
    if match := number_phone(phone):
        print(f"Phone: {match.group()}")
    else:
        print(f"No phone number found in: {phone}")
