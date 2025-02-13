import re


def find_urls(text):
    """Finds all URLs in a given text.
    This function uses a regular expression to search for URLs starting with "http://" or "https://".
    """
    pattern = r"https?://[^\s]+"
    return re.findall(pattern, text)


text_urls = "Welcome to https://welcome.com"
print(find_urls(text_urls))
