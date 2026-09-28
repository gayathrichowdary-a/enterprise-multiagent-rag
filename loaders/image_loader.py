import os
from langchain_core.documents import Document
from PIL import Image

def load_image(file_path):
    """
    Extracts text from images using pytesseract OCR if available,
    with robust error handling and fallback parsing.
    """
    extracted_text = ""
    try:
        import pytesseract
        for cmd in [r"C:\Program Files\Tesseract-OCR\tesseract.exe", "/usr/bin/tesseract"]:
            if os.path.exists(cmd):
                pytesseract.pytesseract.tesseract_cmd = cmd
                break
        img = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(img).strip()
    except Exception:
        extracted_text = ""

    if not extracted_text:
        filename = os.path.basename(file_path)
        extracted_text = f"Scanned Visual / Diagram Asset: {filename}\nImage entity registered in knowledge base."

    return [Document(page_content=extracted_text, metadata={"source": file_path, "type": "image_ocr"})]
