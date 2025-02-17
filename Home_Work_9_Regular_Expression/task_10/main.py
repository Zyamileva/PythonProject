import re


def extract_image_urls(text_with_images) -> list[str] | None:
    """Extracts image URLs from a given text.

    This function uses a regular expression to find URLs ending with common image extensions (jpg, jpeg, png, svg) within the input string.

    Args:
        text_with_images: The input string containing image URLs.

    Returns:
        A list of strings, where each string is an image URL found in the input text, or None if no image URLs are found.
    """
    pattern = r"https?://[^\s]+?\.(?:jpg|jpeg|png|svg)"
    return re.findall(pattern, text_with_images)


text = """
Ось картинки: https://example.com/image1.jpg, https://site.org/pic.png.
Ще одне: http://images.net/photo.jpeg і https://cdn.com/logo.svg.
"""

image_urls = extract_image_urls(text)
print(image_urls)
