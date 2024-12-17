from flask import Flask, request, jsonify
import fitz  # PyMuPDF for PDF processing

app = Flask(__name__)

@app.route('/api/extract', methods=['POST'])
def extract_text():
    data = request.json
    pdf_base64 = data.get('pdf_base64')

    try:
        pdf_data = fitz.open(stream=base64.b64decode(pdf_base64), filetype="pdf")
        text = ""
        for page in pdf_data:
            text += page.get_text()

        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
