import requests
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

class AIController:
    def __init__(self, external_service, internal_service, db_context):
        self.external_service = external_service
        self.internal_service = internal_service
        self.db_context = db_context

    async def process_text_externally(self, text):
        return await self.external_service.process_text(text)

    async def process_text_internally(self, text):
        return await self.internal_service.process_text(text)

class MainController:
    def __init__(self, ai_controller, text_extractor_url, db_context):
        self.ai_controller = ai_controller
        self.text_extractor_url = text_extractor_url
        self.db_context = db_context

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

    async def process_text(self, text, user_id):
        """
        Use the AIController to process the extracted text based on the user ID.
        """
        user_info = await self.db_context.get_user_info_async(user_id)
        if user_info['credit_balance'] > 100:
            return await self.ai_controller.process_text_externally(text)
        else:
            return await self.ai_controller.process_text_internally(text)

'''
class DatabaseContext:
    def __init__(self, db_url="postgresql://db_admin:password123@localhost:5432/main_db"):
        # Initialize the database connection
        self.db_url = db_url

    def _get_db_connection(self):
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(self.db_url)
        return conn

    async def get_user_info_async(self, user_id):
        # Fetch user info based on user_id (e.g., credit balance)
        conn = self._get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("SELECT credit_balance FROM users WHERE user_id = %s", (user_id,))
            user_info = cursor.fetchone()
            if user_info:
                return user_info
            return {"credit_balance": 0}
        except Exception as ex:
            return {"error": f"Failed to fetch user info: {str(ex)}"}
        finally:
            cursor.close()
            conn.close()
'''

class AiExternalService:
    async def process_text(self, text: str):
        return f"Processed externally: {text}"

class AiInternalService:
    async def process_text(self, text: str):
        return f"Processed internally: {text}"


# Flask Setup
app = Flask(__name__)

# Initialize DatabaseContext
# db_context = DatabaseContext()

# Create instances of the services
external_service = AiExternalService()
internal_service = AiInternalService()

# Create the AIController
ai_controller = AIController(external_service, internal_service, db_context)

# Create the MainController
main_controller = MainController(ai_controller, "http://209.38.252.155:5001/api/extract", db_context)


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
