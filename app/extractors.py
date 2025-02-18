from fastapi import UploadFile, HTTPException
import fitz 
import docx
import io

def extract_text(file: UploadFile):
    """Extracts text from a PDF or DOCX file."""
    file.file.seek(0) 
    if file.filename.endswith(".pdf"):
        doc = fitz.open(stream=file.file.read(), filetype="pdf")
        return "\n".join([page.get_text("text") for page in doc])
    elif file.filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(file.file.read()))
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format. Only PDF and DOCX are allowed.")
