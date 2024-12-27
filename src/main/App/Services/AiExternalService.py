import requests

class AIExternalService:
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url

    async def process_text(self, text: str):
        """
        Send a request to the GroqCloud API to process the given text.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": text}]
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                return response_data['choices'][0]['message']['content']
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as ex:
            return f"Exception: {str(ex)}"
