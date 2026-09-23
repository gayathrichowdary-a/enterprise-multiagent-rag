import csv
class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}

def load_csv(file_path):
    rows = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        for r in reader:
            rows.append(", ".join(r))
    return [Document(page_content="\n".join(rows), metadata={"source": file_path})]
