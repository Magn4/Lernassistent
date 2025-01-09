from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

from Database.DatabaseContext import DatabaseContext

from Controllers.TextController import TextController
from Controllers.AIController import AIController
from Controllers.UserController import UserController

from Services.TextExtractor import TextExtractor
from Services.AITextProcessor import AITextProcessor
from Services.AIExternalService import AIExternalService
from Services.AILocalService import AILocalService
from Services.UserService import UserService

# Flask Setup
app = Flask(__name__)

# Create instances of the services
api_key = "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"
api_url = "https://api.groq.com/openai/v1/chat/completions"
local_api_url = "http://127.0.0.1:9191/api/generate"
text_extractor_url = "http://127.0.0.1/extract_pdf/api/extract"



external_service = AIExternalService(api_key, api_url)
local_service = AILocalService(local_api_url)
ai_controller = AIController(external_service, local_service)
text_extractor = TextExtractor(text_extractor_url)
AI_text_processor = AITextProcessor(ai_controller)

# Create the TextController
text_controller = TextController(text_extractor, AI_text_processor)

# Create the UserService and UserController
db_context = DatabaseContext()
user_service = UserService(db_context)
user_controller = UserController(user_service)

<<<<<<< HEAD

=======
@app.errorhandler(Exception)
def handle_exception(e):
    response = {
        "error": str(e)
    }
    if isinstance(e, HTTPException):
        response["code"] = e.code
    else:
        response["code"] = 500
    return jsonify(response), response["code"]
>>>>>>> d7edf03bfcdf47d0065ccee46b98f372c0c3d078

@app.route('/process_pdf', methods=['POST'])
async def process_pdf():
    try:
        data = request.form
        user_id = data.get('user_id')
        use_local = data.get('use_local', 'false').lower() == 'true'
        instruction = data.get('instruction', '')

<<<<<<< HEAD

    pdf_file = request.files.get('file')
    if not pdf_file:
        return jsonify({"error": "No PDF file provided"}), 400
=======
>>>>>>> d7edf03bfcdf47d0065ccee46b98f372c0c3d078

        pdf_file = request.files.get('file')
        if not pdf_file:
            return jsonify({"error": "No PDF file provided"}), 400

        pdf_data = pdf_file.read()
        print("PDF data received")  # Log the receipt of the PDF data

        extracted_text = text_controller.convert_to_text(pdf_data)
        # print(f"Extracted text: {extracted_text}")  # Log extracted text or error message

        if "Error" in extracted_text or "Exception" in extracted_text:
            return jsonify({"error": extracted_text}), 500

        result = await text_controller.process_text(extracted_text, user_id, use_local, instruction)
        print(f"Processing result: {result}")  # Log result from AI processing

        return jsonify({"result": result})
    except Exception as e:
        return handle_exception(e)

@app.route('/register', methods=['POST'])
def register():
    try:
        return user_controller.register()
    except Exception as e:
        return handle_exception(e)

@app.route('/login', methods=['POST'])
def login():
    try:
        return user_controller.login()
    except Exception as e:
        return handle_exception(e)

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        return user_controller.get_all_users()
    except Exception as e:
        return handle_exception(e)

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)

<<<<<<< HEAD
 
=======
>>>>>>> d7edf03bfcdf47d0065ccee46b98f372c0c3d078
