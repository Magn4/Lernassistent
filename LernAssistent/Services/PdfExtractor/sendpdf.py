import requests

# Path to the PDF file you want to send
pdf_path = r"C:\Users\hp\Desktop\Informatik\5. Semester\Informatik Projekt\Sample pdf Test.pdf"


# The URL of your Flask endpoint
url = "http://127.0.0.1:5001/api/extract"

# Open the PDF file in binary mode and send it as part of the POST request
with open(pdf_path, "rb") as pdf_file:
    files = {'file': pdf_file}
    response = requests.post(url, files=files)

# Print the response from the server
if response.status_code == 200:
    result = response.json()
    print("Extracted Text:", result.get("text"))
else:
    print("Error:", response.json())
