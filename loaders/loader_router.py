import os

class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}

def load_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    # DOCX: Extract from BOTH paragraphs and tables (crucial for resumes!)
    if ext in [".docx", ".doc"]:
        try:
            import docx
            doc = docx.Document(file_path)
            lines = []
            for p in doc.paragraphs:
                if p.text.strip():
                    lines.append(p.text.strip())
            for table in doc.tables:
                for row in table.rows:
                    row_texts = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_texts:
                        lines.append(" | ".join(row_texts))
            text = "\n".join(lines)
        except Exception:
            text = ""

    # PDF
    elif ext == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            for page in reader.pages:
                t = page.extract_text()
                if t: text += t + "\n"
        except Exception:
            pass

    # TXT / CSV / JSON
    elif ext in [".txt", ".csv", ".json"]:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception:
            pass

    if not text.strip():
        text = f"Document content from {os.path.basename(file_path)}"

    return [Document(page_content=text, metadata={"source": file_path, "file_name": os.path.basename(file_path)})]
