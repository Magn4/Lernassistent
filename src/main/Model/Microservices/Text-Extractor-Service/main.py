from fastapi import FastAPI, File, UploadFile
import fitz  # PyMuPDF for PDF processing
from docx import Document
import io

app = FastAPI()

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    # Check the file type and process accordingly
    if file.content_type == "application/pdf":
        text = extract_text_from_pdf(await file.read())
    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(await file.read())
    else:
        return {"error": "Unsupported file type"}
    return {"text": text}

def extract_text_from_pdf(pdf_file: bytes):
    # Use the provided byte data to load the PDF
    pdf_document = fitz.open(stream=pdf_file, filetype="pdf")
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text

def extract_text_from_docx(docx_file: bytes):
    # Create a file-like object from the byte data
    doc = Document(io.BytesIO(docx_file))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text
