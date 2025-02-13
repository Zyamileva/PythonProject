import re


def delete_html_tags(text_tags: str) -> str:
    """Reformats dates from DD/MM/YYYY to YYYY-MM-DD format.
    This function uses a regular expression to find and replace dates in the input string.
    """
    return re.sub(r"<.*?>", "", text_tags)


text = '<body><h1>Заголовок страницы</h1> <p>Это абзац с <b>жирным</b> и <i>курсивным</i> текстом.</p> <a href="https://example.com">Перейти на сайт</a></body></html>'
print(delete_html_tags(text))
