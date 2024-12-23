import requests
from flask import Flask, request, jsonify
import json
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from main.App.Services.AiExternalService import AiExternalService
from main.App.Services.AiInternalService import AiInternalService

# Database connection settings
DATABASE_URL = "postgresql://db_admin:password123@localhost:5432/main_db"  # Updated to match your Docker setup

# SQLAlchemy setup
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    credit_balance = Column(Integer)

# DatabaseContext with SQLAlchemy
class DatabaseContext:
    def __init__(self, db_url=DATABASE_URL):
        # Initialize the database connection
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self._initialize_database()

    def _initialize_database(self):
        """
        Create the necessary tables if they do not exist.
        """
        Base.metadata.create_all(self.engine)

    def get_user_info(self, user_id):
        """
        Fetch user info based on user_id (e.g., credit balance)
        """
        session = self.Session()
        try:
            user = session.query(User).filter_by(user_id=user_id).first()
            if user:
                return {"credit_balance": user.credit_balance}
            return {"credit_balance": 0}  # Default value if user not found
        except Exception as ex:
            return {"error": f"Failed to fetch user info: {str(ex)}"}
        finally:
            session.close()

# MainController and AIController classes (same as before)
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
        user_info = self.db_context.get_user_info(user_id)
        if user_info['credit_balance'] > 100:
            return await self.ai_controller.process_text_externally(text)
        else:
            return await self.ai_controller.process_text_internally(text)


# Flask Setup
app = Flask(__name__)

# Initialize DatabaseContext (this will automatically create the users table if not exists)
db_context = DatabaseContext()

# Create instances of the services
external_service = AiExternalService()
internal_service = AiInternalService()

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
