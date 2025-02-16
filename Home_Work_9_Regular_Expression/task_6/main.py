import re


def is_valid_password(password) -> bool:
    """Checks if a given password meets certain criteria.

    This function uses a regular expression to validate the strength of a password.

    Args:
        password: The password string to be validated.

    Returns:
        True if the password meets the criteria, False otherwise.
    """
    return bool(
        re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&*!?]).{8,}$", password)
    )


print(is_valid_password("HELLO"))
print(is_valid_password("HelloWork1@"))
print(is_valid_password("123456789"))
print(is_valid_password("HelloWork"))
