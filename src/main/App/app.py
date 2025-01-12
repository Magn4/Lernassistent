from flask import Flask, request, jsonify

from Controllers.DashboardController import DashboardController
from Database.DatabaseContext import DatabaseContext
from Controllers.TextController import TextController
from Controllers.AIController import AIController
from Controllers.UserController import UserController
from Services.TextExtractor import TextExtractor
from Services.AITextProcessor import AITextProcessor
from Services.AIExternalService import AIExternalService
from Services.AILocalService import AILocalService
from Services.UserService import UserService
from Services.InstructionProcessor import InstructionProcessor   # Import the new class

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

# Code for Instruction

@app.route('/process_pdf', methods=['POST'])
async def process_pdf():
    data = request.form
    user_id = data.get('user_id')
    use_local = data.get('use_local', 'false').lower() == 'true'
    instruction = data.get('instruction', '')

    # Check if instruction was provided
    if not instruction:
        return jsonify({"error": "Instruction is required"}), 400  # Make sure the instruction is provided

    pdf_file = request.files.get('file')
    if not pdf_file:
        return jsonify({"error": "No PDF file provided"}), 400  # Ensure that a PDF file is uploaded

    pdf_data = pdf_file.read()
    print("PDF data received")  # Log the receipt of the PDF data

    # Extract the text from the uploaded PDF
    extracted_text = text_controller.convert_to_text(pdf_data)
    # print(f"Extracted text: {extracted_text}")  # Log extracted text or error message

    # Handle errors in case text extraction fails
    if "Error" in extracted_text or "Exception" in extracted_text:
        return jsonify({"error": extracted_text}), 500

    # Create an instance of InstructionProcessor with the necessary API details
    api_key = "your-api-key"
    external_api_url = "https://api.groq.com/openai/v1/chat/completions"
    local_api_url = "http://localhost:9191/api/generate"

    # Instantiate the InstructionProcessor
    instruction_processor = InstructionProcessor(api_key, external_api_url, local_api_url)

    # Process the extracted text with the instruction provided (either summary or explanation)
    if "summary" in instruction.lower():
        result = await instruction_processor.get_summary(extracted_text, use_local)
    elif "explanation" in instruction.lower():
        result = await instruction_processor.get_explanation(extracted_text, use_local)
    else:
        return jsonify({"error": "Invalid instruction. Please use 'summary' or 'explanation'."}), 400  # Invalid instruction error

    print(f"Processing result: {result}")  # Log result from AI processing

    # Return the AI-generated result to the client
    return jsonify({"result": result})

# **New Endpoint for Dashboard File Upload (This is the new part)**
@app.route('/upload_dashboard', methods=['POST'])
def upload_dashboard():
    # Retrieve form data from the request (sent from the frontend)
    data = request.form
    module_name = data.get('moduleName')  # Get the module name
    directory_name = data.get('directoryName')  # Get the directory name

    # Check if the required data is provided
    if not module_name or not directory_name:
        return jsonify({"error": "Module name and Directory name are required"}), 400

    # Retrieve the PDF file uploaded from the frontend
    pdf_file = request.files.get('file')
    if not pdf_file:
        return jsonify({"error": "No PDF file provided"}), 400

    # Ensure the file is in PDF format
    if not pdf_file.filename.endswith('.pdf'):
        return jsonify({"error": "The file must be in PDF format"}), 400

    # Set the module name and directory name in the DashboardController
    dashboard_controller.set_module_name(module_name)
    dashboard_controller.set_directory_name(directory_name)

    # Extract text from the PDF file using the method from the DashboardController
    extracted_text = dashboard_controller.extract_text_from_pdf(pdf_file)

    # If there's an error while extracting text, return it
    if "Error" in extracted_text:
        return jsonify({"error": extracted_text}), 500

    # Send a successful response with the extracted text and the set names
    return jsonify({
        "message": "File uploaded successfully",
        "module_name": dashboard_controller.module_name,
        "directory_name": dashboard_controller.directory_name,
        "extracted_text": extracted_text  # Optional, depending if you want to return the extracted text
    }), 200


@app.route('/register', methods=['POST'])
def register():
    return user_controller.register()

@app.route('/login', methods=['POST'])
def login():
    return user_controller.login()

@app.route('/users', methods=['GET'])
def get_all_users():
    return user_controller.get_all_users()

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)

