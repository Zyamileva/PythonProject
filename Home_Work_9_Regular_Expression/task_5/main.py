import re


def delete_html_tags(text_tags: str) -> str:
    """Removes HTML tags from a given string.

    This function uses a regular expression to find and remove all HTML tags in the input string.

    Args:
        text_tags: The input string containing HTML tags.

    Returns:
        The input string with all HTML tags removed.
    """
    return re.sub(r"<.*?>", "", text_tags)


text = '<body><h1>Заголовок страницы</h1> <p>Это абзац с <b>жирным</b> и <i>курсивным</i> текстом.</p> <a href="https://example.com">Перейти на сайт</a></body></html>'
print(delete_html_tags(text))
