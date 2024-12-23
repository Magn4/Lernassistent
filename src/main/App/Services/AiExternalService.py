import requests

class AiExternalService:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url  # Base URL for the external API
        self.api_key = api_key  # API Key for authentication

    async def process_text(self, text: str) -> str:
        # Prepare the data to send to the API
        data = {
            "text": text,
            "api_key": self.api_key
        }

        try:
            # Send POST request to the external API
            response = requests.post(self.api_url, json=data)
            # If the request was successful, process the response
            if response.status_code == 200:
                result = response.json()
                return result.get('processed_text', 'No processed text returned')
            else:
                return f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.RequestException as e:
            return f"Request error: {str(e)}"
