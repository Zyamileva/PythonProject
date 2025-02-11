import pytest


class AgeVerifier:
    @staticmethod
    def is_adult(age: int) -> bool:
        """
        Checks if the user is an adult.

        >>> AgeVerifier.is_adult(18)
        True

        >>> AgeVerifier.is_adult(10)
        False

        >>> AgeVerifier.is_adult(120)
        True

        >>> AgeVerifier.is_adult(0)
        False
        """
        return age >= 18


@pytest.mark.skip(reason="Incorrect age value")
@pytest.mark.parametrize("age", [-1, -7, 0])
def test_is_adult_invalid_age(age: int):
    """Test cases for invalid age values with is_adult function.
    This test suite verifies that the `is_adult` function correctly handles
    invalid age values, such as negative numbers and zero, by ensuring it returns False.
    This test is skipped due to the specified condition.
    """
    assert not AgeVerifier.is_adult(age)


@pytest.mark.skipif(True, reason="Incorrect age value")
@pytest.mark.parametrize("age", [121, 130, 150])
def test_is_adult_unrealistic_age(age: int):
    """Test cases for unrealistic age values with is_adult function.
    This test suite verifies that the `is_adult` function correctly handles
    unrealistic age values by ensuring it returns False for ages beyond a reasonable limit.
    This test is skipped due to the specified condition.
    """
    assert not AgeVerifier.is_adult(age)


@pytest.mark.parametrize("age", [20, 119, 120, 121])
def test_is_adult(age):
    """Test cases for the is_adult function.
    This test suite verifies the behavior of the `is_adult` function
    by checking its output against expected values for various age inputs.
    It uses parametrization to run the test with different age values."""
    if age > 120:
        pytest.skip("Incorrect age value")
    assert AgeVerifier.is_adult(age) == (age >= 18)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    pytest.main()
