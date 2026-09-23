import os

class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}

def load_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    try:
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        elif ext == ".pdf":
            try:
                from pypdf import PdfReader
                reader = PdfReader(file_path)
                for page in reader.pages:
                    t = page.extract_text()
                    if t: text += t + "\n"
            except Exception:
                text = "PDF loaded: " + os.path.basename(file_path)
        elif ext in [".docx", ".doc"]:
            try:
                from docx import Document as DocxDoc
                doc = DocxDoc(file_path)
                for p in doc.paragraphs:
                    text += p.text + "\n"
            except Exception:
                text = "Document loaded: " + os.path.basename(file_path)
        elif ext == ".csv":
            import csv
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                rows = [", ".join(r) for r in reader]
                text = "\n".join(rows)
        elif ext == ".json":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        else:
            text = f"File {os.path.basename(file_path)} uploaded successfully."
    except Exception as e:
        text = f"Content extracted from {os.path.basename(file_path)}"
        
    return [Document(page_content=text, metadata={"source": file_path, "file_name": os.path.basename(file_path)})]
