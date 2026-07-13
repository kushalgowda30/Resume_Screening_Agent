import fitz  # PyMuPDF
from docx import Document
import os


def extract_pdf_text(pdf_path):
    text = ""

    doc = fitz.open(pdf_path)

    print("Pages:", len(doc))

    for i, page in enumerate(doc):
        page_text = page.get_text("text")
        print(f"Page {i+1} characters:", len(page_text))
        text += page_text

    doc.close()

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