# app/Controllers/DashboardController.py


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

    # Extract text from a given PDF file using the TextExtractor service.
    
    def extract_text_from_pdf(self, pdf_data):
        try:
            # Importiere TextExtractor innerhalb der Methode, nicht oben
            from Services.TextExtractor import TextExtractor
            
            # Verwende TextExtractor hier
            text_extractor = TextExtractor("http://209.38.252.155/extract_pdf/api/extract")
            return text_extractor.convert_to_text(pdf_data)
        except Exception as e:
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
