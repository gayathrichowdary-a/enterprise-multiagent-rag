# loaders/docx_loader.py
from docx import Document

try:
    from langchain_core.documents import Document as LangDocument
except ImportError:
    try:
        from langchain.schema import Document as LangDocument
    except ImportError:
        # Standalone fallback class (works even without langchain!)
        class LangDocument:
            def __init__(self, page_content, metadata=None):
                self.page_content = page_content
                self.metadata = metadata or {}


def load_docx(file_path):
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"

    return [
        LangDocument(
            page_content=text,
            metadata={"source": file_path}
        )
    ]