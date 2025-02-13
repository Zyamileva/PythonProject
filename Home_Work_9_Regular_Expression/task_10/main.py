import re


def extract_image_urls(text_with_images):
    """Extracts image URLs from a given text.
    Finds all URLs ending with common image extensions (jpg, jpeg, png, svg) in a string using a regular expression.
    """
    pattern = r"https?://[^\s]+?\.(?:jpg|jpeg|png|svg)"
    return re.findall(pattern, text_with_images)


text = """
Ось картинки: https://example.com/image1.jpg, https://site.org/pic.png.
Ще одне: http://images.net/photo.jpeg і https://cdn.com/logo.svg.
"""

image_urls = extract_image_urls(text)
print(image_urls)
