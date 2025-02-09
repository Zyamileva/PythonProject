import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import unittest
from main import StringProcessor


class TestString(unittest.TestCase):
    """A class to test string processing methods.
    This class uses the unittest framework to test the functionality of the StringProcessor class.
    It includes tests for reversing, capitalizing, and counting vowels in strings.
    """

    def setUp(self):
        """Set up for test methods.
        Instantiates a StringProcessor object.
        """
        self.processor = StringProcessor()

    @unittest.skip("We plan to decide later.")
    def test_reverse_string_empty(self):
        """Test reversing an empty string.
        Checks that reversing an empty string returns an empty string.
        """
        self.assertEqual(self.processor.reverse_string(""), "")

    def test_reverse_string(self):
        """Test reversing a string.
        Checks that reversing a string returns the expected reversed string.
        """
        self.assertEqual(self.processor.reverse_string("hello"), "olleh")

    def test_reverse_string_symbol(self):
        """Test reversing a string with a symbol.
        Checks that reversing a string with a symbol returns the reversed string with the symbol at the beginning.
        """
        self.assertEqual(self.processor.reverse_string("123&"), "&321")

    def test_reverse_string_mix(self):
        """Test reversing a mixed string.
        Checks that reversing a string with mixed characters returns the correctly reversed string.
        """
        self.assertEqual(self.processor.reverse_string("12N3"), "3N21")

    def test_capitalize_string(self):
        """Test reversing a mixed string.

        Checks that reversing a string with mixed characters returns the correctly reversed string.
        """
        self.assertEqual(
            self.processor.capitalize_string("hello World!"), "Hello world!"
        )

    def test_capitalize_string_empty(self):
        """Test capitalizing an empty string.
        Checks that capitalizing an empty string returns an empty string.
        """
        self.assertEqual(self.processor.capitalize_string(""), "")

    def test_capitalize_string_symbol(self):
        """Test capitalizing a string with a symbol.
        Checks that capitalizing a string with a symbol as the first character returns the original string.
        """
        self.assertEqual(self.processor.capitalize_string("12@3"), "12@3")

    def test_capitalize_string_mix(self):
        """Test capitalizing a mixed string.
        Checks that capitalizing a mixed string returns the string with the first letter capitalized and the rest lowercased.
        """
        self.assertEqual(self.processor.capitalize_string("1lolL!"), "1loll!")

    def test_count_vowels(self):
        """Test counting vowels in a string.
        Checks that the function correctly counts the number of vowels in a given string.
        """
        self.assertEqual(self.processor.count_vowels("hello world!"), 3)

    def test_count_vowels_symbol(self):
        """Test counting vowels in a string with symbols.
        Checks that the function correctly returns 0 when the input string contains no vowels.
        """
        self.assertEqual(self.processor.count_vowels("123$"), 0)

    def test_count_mix(self):
        """Test counting vowels in a mixed string.
        Checks that the function correctly counts vowels in a string containing a mix of alphanumeric and special characters.
        """
        self.assertEqual(self.processor.count_vowels("1230 %world!"), 1)

    def test_count_vowels_empty(self):
        """Test counting vowels in an empty string.
        Checks that the function correctly returns 0 for an empty string.
        """
        self.assertEqual(self.processor.count_vowels(""), 0)


if __name__ == "__main__":
    unittest.main()
