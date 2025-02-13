import re


def is_valid_email(email_text: str) -> bool:
    """Checks if a given string is a valid email address.
    This function uses a regular expression to validate the format of an email address.
    """
    re_email = re.compile(
        r"^[A-za-z0-9]+(\.[A-za-z0-9]+)*@[A-za-z0-9]+\.[A-za-z]{2,6}$"
    )
    return bool(re_email.match(email_text))


emails = [
    "lena.ivanova@example.com",
    "i.tany28@gmail.com",
    "petrov555@ukr.net",
    ".My@ukr.net",
    "olena.@ukr.net",
]

for email in emails:
    print(f"{email}: {is_valid_email(email)}")
