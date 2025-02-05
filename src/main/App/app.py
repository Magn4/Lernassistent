from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

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
from Services.InstructionProcessor import InstructionProcessor  # Import the new class

# Flask Setup
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
# Configuration
app.config['UPLOAD_FOLDER'] = 'C:/Users/hp/Desktop/Uploads'  # Set this to the desired upload folder path

# Create an instance of the DatabaseContext
db_context = DatabaseContext()


# Create an instance of the DashboardController (with the db_context passed in)
dashboard_controller = DashboardController(db_context)


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
instruction_processor = InstructionProcessor(api_key, api_url, local_api_url)


# Create the TextController
text_controller = TextController(text_extractor, AI_text_processor)

# Create the UserService and UserController
user_service = UserService(db_context)
user_controller = UserController(user_service)
file_manager_controller = FileManagerController(db_context)

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


# Endpoints for PDF Processing with Summary and Explanation Features

@app.route('/get_summary', methods=['POST'])
async def get_summary():
    # Retrieve data from the POST request
    data = request.form
    use_local = data.get('use_local', 'false').lower() == 'true'

    # Get the optional title from the form data
    title = data.get('title')  # Title can be passed with the request

    pdf_file = request.files.get('file')
    if not pdf_file:
        return jsonify({"error": "No PDF file provided"}), 400

    pdf_data = pdf_file.read()
    extracted_text = text_controller.convert_to_text(pdf_data)

    if "Error" in extracted_text or "Exception" in extracted_text:
        return jsonify({"error": extracted_text}), 500

    # Check if the summary already exists in the database
    existing_summary = db_context.find_summary_by_text(extracted_text)
    if existing_summary:
        return jsonify({
            "status": "success",
            "data": {
                "summary": existing_summary.summary_text,
                "title": existing_summary.title,
                "details": {
                    "length": len(existing_summary.summary_text),
                    "generated_with": "cached_result",
                }
            }
        })

    # Generate a new summary if not found
    result = await instruction_processor.get_summary(extracted_text, use_local)

    # Save the new summary in the database, including the optional title
    summary_id = db_context.save_summary(extracted_text, result['data']['summary'], title=title)

    return jsonify({
        "status": "success",
        "data": {
            "summary": result['data']['summary'],
            "summary_id": summary_id,
            "details": {
                "length": len(result['data']['summary']),
                "generated_with": "external_ai" if not use_local else "local_ai",
            }
        }
    })


@app.route('/get_explanation', methods=['POST'])
async def get_explanation():
    # Retrieve data from the POST request
    data = request.form
    # Check if 'use_local' is provided, and convert it to a boolean (default: False)
    use_local = data.get('use_local', 'false').lower() == 'true'

    # Retrieve the uploaded PDF file from the request
    pdf_file = request.files.get('file')
    if not pdf_file:
        # Return an error if no file was provided
        return jsonify({"error": "No PDF file provided"}), 400

    # Read the file data from the uploaded PDF
    pdf_data = pdf_file.read()
    print("PDF data received")  # Log the receipt of the file for debugging purposes

    # Extract the text from the uploaded PDF using the TextController
    extracted_text = text_controller.convert_to_text(pdf_data)

    # Check if there was an error during text extraction
    if "Error" in extracted_text or "Exception" in extracted_text:
        # Return an error response if text extraction failed
        return jsonify({"error": extracted_text}), 500

    # Process the extracted text to generate a detailed explanation
    result = await instruction_processor.get_explanation(extracted_text, use_local)
    print(f"Explanation result: {result}")  # Log the result of the explanation processing

    # Return the generated explanation to the client
    return jsonify({"result": result})



@app.route('/files/<module_name>/<topic_name>/<filename>', methods=['GET'])
def open_file(module_name, topic_name, filename):
    return file_manager_controller.open_file(module_name, topic_name, filename)

@app.route('/download_file/<module_name>/<topic_name>/<filename>', methods=['GET'])
def download_file(module_name, topic_name, filename):
    return file_manager_controller.download_file(module_name, topic_name, filename)

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

@app.route('/create_module', methods=['POST'])
def create_module():
    return file_manager_controller.create_module()

@app.route('/create_topic', methods=['POST'])
def create_topic():
    return file_manager_controller.create_topic()

@app.route('/upload_file', methods=['POST'])
def upload_file():
    return file_manager_controller.upload_file()

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        return user_controller.get_all_users()
    except Exception as e:
        return handle_exception(e)

@app.route('/modules', methods=['GET'])
def list_modules():
    return file_manager_controller.list_modules()

@app.route('/modules/<module_name>/topics', methods=['GET'])
def list_topics(module_name):
    return file_manager_controller.list_topics(module_name)

@app.route('/modules/<module_name>/topics/<topic_name>/files', methods=['GET'])
def list_files(module_name, topic_name):
    return file_manager_controller.list_files(module_name, topic_name)

@app.route('/delete_module/<module_name>', methods=['DELETE'])
def delete_module(module_name):
    return file_manager_controller.delete_module(module_name)

@app.route('/delete_topic/ ', methods=['DELETE'])
def delete_topic(module_name, topic_name):
    return file_manager_controller.delete_topic(module_name, topic_name)

@app.route('/files/<module_name>/<topic_name>/<filename>', methods=['DELETE'])
def delete_file(module_name, topic_name, filename):
    return file_manager_controller.delete_file(module_name, topic_name, filename)



# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)

