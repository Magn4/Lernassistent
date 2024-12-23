import requests
import json

class TextController:
    def __init__(self):
        # Base URL for Flask microservice
        # self.base_url = "http://localhost:5001/api/extract"
        self.base_url = "http://209.38.252.155:5001/api/extract"

    def convert_to_text(self, pdf_data):
        """
        Converts a PDF to text by calling an external microservice.

        :param pdf_data: The binary data of the PDF file.
        :return: The extracted text or an error message.
        """
        files = {
            'file': ('uploaded.pdf', pdf_data, 'application/pdf')
        }

        try:
            # Send POST request to Flask microservice with the PDF data
            response = requests.post(self.base_url, files=files)
            
            if response.status_code == 200:
                # Parse JSON response
                response_data = response.json()
                return response_data.get('text', 'No text extracted')
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as ex:
            return f"Exception: {str(ex)}"


def process_pdf(file_path):
    """
    Process the PDF file, read its content and pass it to TextController for text extraction.

    :param file_path: The path to the PDF file.
    :return: The extracted text from the PDF or an error message.
    """
    # Initialize TextController
    controller = TextController()
    
    try:
        with open(file_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
        
        # Get extracted text
        extracted_text = controller.convert_to_text(pdf_data)
        return extracted_text
    except Exception as ex:
        return f"Failed to process the PDF file: {str(ex)}"


# Example usage:
if __name__ == '__main__':
    pdf_path = "/Users/taha/Desktop/001_Taha/002_Studium/002_Uni/001_Fank_UAS/Uni/5.Semester/NachSchreib/Dist_Sys/Lectures/07_blockchains.pdf"
    
    # Call the function to process the PDF
    extracted_text = process_pdf(pdf_path)
    
    # Print the extracted text
    print(extracted_text)
