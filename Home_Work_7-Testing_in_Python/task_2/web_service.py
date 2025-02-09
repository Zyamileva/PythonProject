import requests


class WebService:
    def get_data(self, url: str) -> dict:
        """
        Sends a GET request to the provided URL and returns the response as a JSON object.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
