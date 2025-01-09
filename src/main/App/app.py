from flask import Flask, request, jsonify

from Controllers.DashboardController import DashboardController


from Database.DatabaseContext import DatabaseContext

from Controllers.TextController import TextController
from Controllers.AIController import AIController
from Controllers.UserController import UserController
from Controllers.FileManagerController import FileManagerController


from Services.TextExtractor import TextExtractor
from Services.AITextProcessor import AITextProcessor
from Services.AIExternalService import AIExternalService
from Services.AILocalService import AILocalService
from Services.UserService import UserService

# Flask Setup
app = Flask(__name__)

# Create an instance of the DatabaseContext
db_context = DatabaseContext()


# Create an instance of the DashboardController (with the db_context passed in)
dashboard_controller = DashboardController(db_context)


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
user_service = UserService(db_context)
user_controller = UserController(user_service)
file_manager_controller = FileManagerController(db_context)



# **New Endpoint for Dashboard File Upload (This is the new part)**

@app.route('/upload_dashboard', methods=['POST'])
def upload_dashboard():
    # Retrieve form data from the request (sent from the frontend)
    data = request.form
    module_name = data.get('moduleName')  # Get the module name
    topic_name = data.get('topicName')  # Get the topic name

    # Check if the required data is provided
    if not module_name or not topic_name:
        return jsonify({"error": "Module name and topic name are required"}), 400

    # Retrieve the PDF file uploaded from the frontend
    pdf_file = request.files.get('file')
    if not pdf_file:
        return jsonify({"error": "No PDF file provided"}), 400

    # Ensure the file is in PDF format
    if not pdf_file.filename.endswith('.pdf'):
        return jsonify({"error": "The file must be in PDF format"}), 400

    # Set the module name and topic name in the DashboardController
    dashboard_controller.set_module_name(module_name)
    dashboard_controller.set_topic_name(topic_name)

    # Extract text from the PDF file using the method from the DashboardController
    extracted_text = dashboard_controller.extract_text_from_pdf(pdf_file)

    # If there's an error while extracting text, return it
    if "Error" in extracted_text:
        return jsonify({"error": extracted_text}), 500

    # Send a successful response with the extracted text and the set names
    return jsonify({
        "message": "File uploaded successfully",
        "module_name": dashboard_controller.module_name,
        "topic_name": dashboard_controller.topic_name,
        "extracted_text": extracted_text  # Optional, depending if you want to return the extracted text
    }), 200


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

@app.route('/users', methods=['GET'])
def get_all_users():
    return user_controller.get_all_users()

@app.route('/create_module', methods=['POST'])
def create_module():
    return file_manager_controller.create_module()

@app.route('/create_topic', methods=['POST'])
def create_topic():
    return file_manager_controller.create_topic()

@app.route('/upload_file', methods=['POST'])
def upload_file():
    return file_manager_controller.upload_file()

@app.route('/delete_module', methods=['DELETE'])
def delete_module():
    return file_manager_controller.delete_module()

@app.route('/delete_topic', methods=['DELETE'])
def delete_topic():
    return file_manager_controller.delete_topic()

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)

 