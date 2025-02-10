from flask import jsonify
import requests
import json
from ..database import AnkiDatabaseContext

class AutoGenerateService:
    def __init__(self):
        self.db_context = AnkiDatabaseContext()

    def auto_generate_cards(self, request):
        try:
            pdf_file = request.files.get('file')
            if not pdf_file:
                return jsonify({"error": "No PDF file provided"}), 400

            if not pdf_file.filename.endswith('.pdf'):
                return jsonify({"error": "The file must be in PDF format"}), 400

            extract_url = "http://127.0.0.1:5001/api/extract"
            files = {'file': pdf_file.read()}
            extract_response = requests.post(extract_url, files=files)

            if extract_response.status_code != 200:
                return jsonify({"error": "Failed to extract text from PDF"}), 500

            extracted_text = extract_response.json().get('text')
            if not extracted_text:
                return jsonify({"error": "No text extracted from PDF"}), 500

            data = {
                "content": extracted_text,
                "deck_id": request.form.get('deck_id'),
                "num_cards": request.form.get('num_cards', 20)
            }

            generate_response = requests.post(
                'http://127.0.0.1:8000/generate-cards',
                json=data
            )

            if generate_response.status_code != 201:
                return jsonify({"error": "Failed to generate cards"}), 500

            return generate_response.json(), 201

        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
