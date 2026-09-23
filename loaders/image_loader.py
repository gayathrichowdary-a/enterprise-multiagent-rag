# loaders/image_loader.py
import os
from langchain_core.documents import Document
from PIL import Image

def load_image(file_path):
    """
    Extracts text from images using pytesseract if installed,
    otherwise provides a safe fallback without crashing the app.
    """
    try:
        import pytesseract
        
        # Check standard Windows Tesseract path if available
        default_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        if os.path.exists(default_tesseract):
            pytesseract.pytesseract.tesseract_cmd = default_tesseract

        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        
        if text.strip():
            return [Document(page_content=text, metadata={"source": file_path, "type": "image"})]
    except Exception as e:
        print(f"[Warning] Tesseract OCR not available: {e}")

    # Safe Fallback: Read file name and basic image info
    filename = os.path.basename(file_path)
    fallback_content = f"Image Document: {filename}\nNote: Visual diagram or scanned asset uploaded ({filename})."
    
    return [Document(page_content=fallback_content, metadata={"source": file_path, "type": "image"})]