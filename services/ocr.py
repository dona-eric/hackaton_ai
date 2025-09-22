import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

def extract_text_from_file(file_path: str) -> dict:
    """
    Extraction OCR page par page.
    Retourne un JSON structuré {page_number: text}
    """
    result = {}

    if file_path.endswith(".pdf"):
        pages = convert_from_path(file_path)
        for i, page in enumerate(pages, start=1):
            text = pytesseract.image_to_string(page)
            result[f"page_{i}"] = text.strip()
    else:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        result["page_1"] = text.strip()

    return result
