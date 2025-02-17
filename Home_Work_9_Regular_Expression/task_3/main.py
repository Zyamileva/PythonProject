import re


def hash_tags(text: str) -> list[str]:
    """Extracts hashtags from a given text.

    This function uses a regular expression to find all hashtags in the input string.

    Args:
        text: The input string to search for hashtags.

    Returns:
        A list of strings, where each string is a hashtag found in the input text.
    """
    return re.findall(r"#\w+", text)


text_search = "Приклад #текст  #хештег #Lesson. Все працює."
print(hash_tags(text_search))
