from flask import Flask, request, jsonify
import fitz  # PyMuPDF for PDF processing
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        # "origins": ["http://maguna.me", "http://localhost", "http://127.0.0.1"],
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": True
    }
})
# Route to handle PDF file upload and extract text
@app.route('/api/extract', methods=['POST'])
def extract_text():
    # Check if the file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']  # Get the uploaded file

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Open the PDF file using PyMuPDF (fitz)
        pdf_data = fitz.open(stream=file.read(), filetype="pdf")  # Read directly from uploaded file
        text = ""

        # Extract text from each page
        for page in pdf_data:
            text += page.get_text()

        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
