import re


def hash_tags(text: str) -> list[str]:
    """Extracts hashtags from a given text.
    Finds all hashtags in a string using a regular expression.
    """
    return re.findall(r"#\w+", text)


text = "Приклад #текст  #хештег #Lesson. Все працює."
print(hash_tags(text))
