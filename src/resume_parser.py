import fitz  # PyMuPDF
from docx import Document
import os


def extract_pdf_text(pdf_path):
    text = ""

    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()

    return text


def extract_docx_text(docx_path):
    doc = Document(docx_path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_resume_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension == ".docx":
        return extract_docx_text(file_path)

    else:
        raise ValueError("Unsupported file format")