# curl -X POST -F "file=@/Users/taha/Desktop/Uni/5.Semester/Op_Sys/Exercices/bts_WS2324_exercise_sheet_01.pdf" http://209.38.252.155:5001/api/extract -i

import requests

# Path to the PDF file you want to send
pdf_path = r"/Users/taha/Desktop/Uni/5.Semester/Op_Sys/Exercices/bts_WS2324_exercise_sheet_01.pdf"

# The URL of your Flask endpoint
url = "http://209.38.252.155:5001/api/extract"

# Open the PDF file in binary mode and send it as part of the POST request
with open(pdf_path, "rb") as pdf_file:
    files = {'file': pdf_file}
    response = requests.post(url, files=files)

# Print the raw response to help with debugging
print("Status Code:", response.status_code)
print("Response Text:", response.text)

# Try to handle JSON response if it exists
if response.status_code == 200:
    try:
        result = response.json()
        print("Extracted Text:", result.get("text"))
    except ValueError:
        print("Error: Received non-JSON response")
else:
    print(f"Error: {response.status_code} - {response.text}")
