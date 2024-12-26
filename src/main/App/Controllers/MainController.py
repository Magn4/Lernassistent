import requests
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor


class AIController:
    def __init__(self, external_service, local_service):
        self.external_service = external_service
        self.local_service = local_service

    async def process_text(self, text, use_local):
        """
        Process the text using either the external or local LLM service based on the flag.
        """
        if use_local:
            return await self.local_service.process_text(text)
        else:
            return await self.external_service.process_text(text)


class MainController:
    def __init__(self, ai_controller, text_extractor_url):
        self.ai_controller = ai_controller
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

    async def process_text(self, text, user_id, use_local):
        """
        Use the AIController to process the extracted text based on the user ID and selected service.
        """
        return await self.ai_controller.process_text(text, use_local)


class AiExternalService:
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


class AiLocalService:
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


# Flask Setup
app = Flask(__name__)

# Create instances of the services
api_key = "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"
api_url = "https://api.groq.com/openai/v1/chat/completions"
local_api_url = "http://209.38.252.155:9191/api/generate"

external_service = AiExternalService(api_key, api_url)
local_service = AiLocalService(local_api_url)

# Create the AIController
ai_controller = AIController(external_service, local_service)

# Create the MainController
main_controller = MainController(ai_controller, "http://209.38.252.155:5001/api/extract")


@app.route('/process_pdf', methods=['POST'])
async def process_pdf():
    data = request.form
    user_id = data.get('user_id')
    use_local = data.get('use_local', 'false').lower() == 'true'

    pdf_file = request.files.get('file')
    if not pdf_file:
        return jsonify({"error": "No PDF file provided"}), 400

    pdf_data = pdf_file.read()
    print("PDF data received")  # Log the receipt of the PDF data

    extracted_text = main_controller.convert_to_text(pdf_data)
    print(f"Extracted text: {extracted_text}")  # Log extracted text or error message

    if "Error" in extracted_text or "Exception" in extracted_text:
        return jsonify({"error": extracted_text}), 500

    result = await main_controller.process_text(extracted_text, user_id, use_local)
    print(f"Processing result: {result}")  # Log result from AI processing

    return jsonify({"result": result})



# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)

