import re


def is_valid_password(password):
    """Checks if a given string is a valid password.
    This function uses a regular expression to validate the format of a password, checking for at least one uppercase letter, one lowercase letter, one digit, one special character, and a minimum length of 8 characters.
    """
    return bool(
        re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&*!?]).{8,}$", password)
    )


print(is_valid_password("HELLO"))
print(is_valid_password("HelloWork1@"))
print(is_valid_password("123456789"))
print(is_valid_password("HelloWork"))
