from flask import Flask, request, jsonify

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
local_api_url = "http://209.38.252.155:9191/api/generate"
text_extractor_url = "http://209.38.252.155/extract_pdf/api/extract"


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



@app.route('/process_pdf', methods=['POST'])
async def process_pdf():
    data = request.form
    user_id = data.get('user_id')
    use_local = data.get('use_local', 'false').lower() == 'true'
    instruction = data.get('instruction', '')


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

@app.route('/register', methods=['POST'])
def register():
    return user_controller.register()

@app.route('/login', methods=['POST'])
def login():
    return user_controller.login()

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)

 