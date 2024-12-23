from flask import Flask, request, jsonify
from src.main.Controllers2.MainController import MainController
from src.main.Controllers2.AiController import AIController
from main.App.Services.AiExternalService import AiExternalService
from main.App.Services.AiInternalService import AiInternalService
from main.App.Database.DatabaseContext import DatabaseContext
import asyncio

# Initialize services and controllers
text_extractor_url = "http://209.38.252.155:5001/api/extract"
db_context = DatabaseContext()

# Create AI services
external_service = AiExternalService()
internal_service = AiInternalService()

# Create AI controller
ai_controller = AIController(external_service, internal_service, db_context)

# Create the MainController
main_controller = MainController(ai_controller, text_extractor_url, db_context)

# Initialize Flask app
app = Flask(__name__)

@app.route('/process_pdf', methods=['POST'])
async def process_pdf():
    """
    API endpoint to receive a PDF, extract text, and process it with AI based on user credit balance.
    """
    # Get the user_id from the request (assuming it's sent in JSON)
    data = request.get_json()
    user_id = data.get('user_id')
    
    # Get the PDF file from the request
    pdf_file = request.files.get('file')
    if not pdf_file:
        return jsonify({"error": "No PDF file provided"}), 400
    
    pdf_data = pdf_file.read()

    # Step 1: Convert PDF to text
    extracted_text = main_controller.convert_to_text(pdf_data)
    if "Error" in extracted_text or "Exception" in extracted_text:
        return jsonify({"error": extracted_text}), 500
    
    # Step 2: Process text using the AIController
    result = await main_controller.process_text(extracted_text, user_id)
    
    # Return the result
    return jsonify({"result": result})


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
