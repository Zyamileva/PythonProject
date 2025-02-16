import re


def find_urls(text) -> list[str] | None:
    """Finds all URLs in a given text.

    This function uses a regular expression to extract all URLs present in the input string.

    Args:
        text: The input string to search for URLs.

    Returns:
        A list of strings, where each string is a URL found in the input text, or None if no URLs are found.
    """
    pattern = r"https?://[^\s]+"
    return re.findall(pattern, text)


text_urls = "Welcome to https://welcome.com"
print(find_urls(text_urls))
