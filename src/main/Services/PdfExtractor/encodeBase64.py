import base64

# Correct path to your PDF file
pdf_path = r"C:\Users\hp\Desktop\Informatik\5. Semester\Informatik Projekt\Sample pdf Test.pdf"

# Encode the PDF file to Base64
with open(pdf_path, "rb") as pdf_file:
    base64_string = base64.b64encode(pdf_file.read()).decode('utf-8')

# Print the Base64-encoded string
print("Base64 Encoded PDF:")
print(base64_string)
