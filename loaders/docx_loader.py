class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}

def load_docx(file_path):
    text = ""
    try:
        from docx import Document as DocxDoc
        doc = DocxDoc(file_path)
        for p in doc.paragraphs:
            text += p.text + "\n"
    except Exception:
        pass
    return [Document(page_content=text or "DOCX loaded", metadata={"source": file_path})]
