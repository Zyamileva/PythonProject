import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import unittest
from unittest.mock import patch, Mock
import requests


from web_service import WebService


class TestWebService(unittest.TestCase):
    """Test suite for the WebService class.
    This test suite covers various scenarios for the get_data method, including success, failure, and error handling.
    """

    def setUp(self):
        """Set up for test methods.
        Instantiates a WebService object and defines the API URL.
        """
        self.service = WebService()
        self.api_url = "https://example.com"

    @patch("requests.get")
    def test_get_data_success(self, mock_get):
        mock_response = Mock(status_code=200, json=lambda: {"data": "test"})
        mock_get.return_value = mock_response

        result = self.service.get_data(self.api_url)
        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once_with(self.api_url)

    @patch("requests.get")
    def test_get_data_fail(self, mock_get: Mock):
        """Test the get_data method with a failed request.
        Simulates a failed API request (status code 404) and checks if the returned result contains the expected error message.
        """
        mock_response = Mock(status_code=404, json=lambda: {"error": "Not Found"})
        mock_get.return_value = mock_response

        result = self.service.get_data(self.api_url)
        self.assertEqual(result, {"error": "Not Found"})
        mock_get.assert_called_once_with(self.api_url)

    @patch("requests.get")
    def test_get_data_error(self, mock_get):
        """Test the get_data method with a connection error.
        Simulates a connection error during the API request and checks if the returned result contains an error message indicating the connection problem.
        """
        mock_get.side_effect = requests.exceptions.ConnectionError(
            "No internet connection"
        )

        result = self.service.get_data(self.api_url)
        self.assertIn("error", result)
        self.assertTrue("No internet connection" in result["error"])
        mock_get.assert_called_once_with(self.api_url)


if __name__ == "__main__":
    unittest.main()
