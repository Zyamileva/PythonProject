class StringProcessor:
    """Provides static methods for string manipulation.
    This class offers a collection of utility functions for common string operations,
    including reversing, capitalizing, and counting vowels."""

    @staticmethod
    def reverse_string(s: str) -> str:
        """Reverses a given string.
        This function takes a string as input and returns its reversed counterpart."""

        return s[::-1]

    @staticmethod
    def capitalize_string(s: str) -> str:
        """Capitalizes the first letter of a given string.
        This function takes a string as input and returns its capitalized version."""

        return s.capitalize()

    @staticmethod
    def count_vowels(s: str) -> int:
        """Counts the number of vowels in a given string.
        This function takes a string as input and returns the count of vowels"""

        return sum(i in "aeiouyAEIOUY" for i in s)
