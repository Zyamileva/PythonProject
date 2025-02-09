import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from main import divide


def test_divide_success():
    """Tests the divide function with successful cases.
    This test case verifies the correct behavior of the divide function with various valid inputs.
    """
    assert divide(8, 2) == 4.0
    assert divide(12, 3) == 4.0
    assert divide(-6, 3) == -2.0
    assert divide(-8, -1) == 8.0
    assert divide(0, 5) == 0.0


def test_divide_by_zero():
    """Tests the divide function with parametrized inputs.
    """
    with pytest.raises(ZeroDivisionError, match="Division by zero is impossible"):
        divide(7, 0)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (12, 2, 6.0),
        (9, 3, 3.0),
        (-6, -2, 3.0),
        (0, 2, 0.0),
        (8, -1, -8.0),
    ],
)
def test_divide_parametrize(a, b, expected):
    """Tests the divide function with various inputs using parametrization.
    This test case verifies the behavior of the divide function with different combinations of dividend and divisor, including positive, negative, and zero values.
    """
    assert divide(a, b) == expected
