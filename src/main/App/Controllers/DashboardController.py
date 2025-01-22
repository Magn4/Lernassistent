# app/Controllers/DashboardController.py

import pdfplumber  # Used to extract text from PDFs
from Database.DatabaseContext import DatabaseContext


class DashboardController:
    def __init__(self, db_context):
        # Initialize the controller with the provided db_context to interact with the database
        self.db_context = db_context  
        self.module_name = None  # Initialize the module_name to None
        self.directory_name = None  # Initialize the directory_name to None

    # Function to set the module name
    def set_module_name(self, module_name):
        self.module_name = module_name  # Set the module name
        print(f"Module name set: {self.module_name}")

    # Function to set the directory name
    def set_directory_name(self, directory_name):
        self.directory_name = directory_name  # Set the directory name
        print(f"Directory name set: {self.directory_name}")

    # Function to extract text from a PDF file
    def extract_text_from_pdf(self, pdf_data):
        try:
            # Open the provided PDF file using pdfplumber
            with pdfplumber.open(pdf_data) as pdf:
                text = ''
                # Iterate through each page of the PDF and extract text
                for page in pdf.pages:
                    text += page.extract_text()
            return text  # Return the extracted text from the PDF
        except Exception as e:
            # Return an error message if the text extraction fails
            return f"Error during text extraction: {str(e)}"

    # Function to save the dashboard upload data to the database
    def save_dashboard_upload(self, extracted_text):
        # Ensure both module name and directory name are set before saving to the database
        if self.module_name and self.directory_name:
            # Save the extracted text and other details (module and directory name) to the database
            self.db_context.save_dashboard_upload(self.module_name, self.directory_name, extracted_text)
            print(f"Dashboard data saved: Module={self.module_name}, Directory={self.directory_name}")
        else:
            # Print an error message if module or directory name is not set
            print("Error: Module name or directory name not set.")
