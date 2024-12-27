import requests

class AILocalService:
    def __init__(self, api_url):
        self.api_url = api_url

    async def process_text(self, text: str):
        """
        Send a request to the local LLM API to process the given text.
        """
        payload = {
            "model": "llama3.2:3b",
            "prompt": text
        }

        try:
            response = requests.post(self.api_url, json=payload)
            if response.status_code == 200:
                # Concatenate the streaming responses
                response_data = response.iter_lines()
                output = ""
                for line in response_data:
                    output += line.decode("utf-8")
                return output
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as ex:
            return f"Exception: {str(ex)}"
