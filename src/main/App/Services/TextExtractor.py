import requests

class TextExtractor:
    def __init__(self, text_extractor_url):
        self.text_extractor_url = text_extractor_url

    def convert_to_text(self, pdf_data):
        """
        Send the PDF data to the TextExtractor microservice to extract text.
        """
        files = {'file': ('uploaded.pdf', pdf_data, 'application/pdf')}
        try:
            response = requests.post(self.text_extractor_url, files=files)
            if response.status_code == 200:
                response_data = response.json()
                return response_data.get('text', 'No text extracted')
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as ex:
            return f"Exception: {str(ex)}"