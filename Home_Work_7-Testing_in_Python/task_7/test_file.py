import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from file_processor import FileProcessor
import pytest


def test_file_write_read(tmpdir):
    """Test for checking methods for reading a file"""
    file = tmpdir.join("testfile.txt")
    FileProcessor.write_to_file(file, "Hello, World!")
    content = FileProcessor.read_from_file(file)
    assert content == "Hello, World!"


def test_large_file(tmpdir):
    """Test for validating methods with large amounts of data"""
    file = tmpdir.join("largeFile.txt")
    large_text = "".join("Hello World!" for _ in range(10**4))
    FileProcessor.write_to_file(file, large_text)
    content = FileProcessor.read_from_file(file)
    assert content == large_text


def test_empty_file(tmpdir):
    """tests to test methods with empty strings"""
    file = tmpdir.join("empty.txt")
    FileProcessor.write_to_file(file, "")
    content = FileProcessor.read_from_file(file)
    assert content == ""


def test_file_not_found():
    """test to check methods for exceptions if the file is not found"""
    file = "not_found.txt"
    with pytest.raises(FileNotFoundError, match="File not found"):
        FileProcessor.read_from_file(file)
