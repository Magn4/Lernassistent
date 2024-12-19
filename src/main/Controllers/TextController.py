import requests
import json



class TextController:
    def __init__(self):
        # Base URL for Flask microservice
        # self.base_url = "http://localhost:5001/api/extract"
        self.base_url = "http://209.38.252.155:5001/api/extract"
    
    def convert_to_text(self, pdf_data):
        # Prepare the file data as part of multipart form-data request
        files = {
            'file': ('uploaded.pdf', pdf_data, 'application/pdf')
        }

        try:
            # Send POST request to Flask microservice with the PDF data
            response = requests.post(self.base_url, files=files)
            
            # Check if the response was successful
            if response.status_code == 200:
                # Parse JSON response
                response_data = response.json()
                # Return the extracted text from the response
                return response_data.get('text', 'No text extracted')
            else:
                # Handle unsuccessful response
                return f"Error: {response.status_code} - {response.text}"
        except Exception as ex:
            # Handle exception (e.g., connection errors)
            return f"Exception: {str(ex)}"

# Example usage:
if __name__ == '__main__':
    # Initialize TextController
    controller = TextController()
    
    # Read the PDF file to be sent
    with open("/Users/taha/Desktop/001_Taha/002_Studium/002_Uni/001_Fank_UAS/Uni/5.Semester/NachSchreib/Dist_Sys/Lectures/07_blockchains.pdf", "rb") as pdf_file:
        pdf_data = pdf_file.read()
    
    # Get extracted text
    extracted_text = controller.convert_to_text(pdf_data)
    
    # Print the extracted text
    print(extracted_text)
