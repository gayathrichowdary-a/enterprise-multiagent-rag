try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except ImportError:
        RecursiveCharacterTextSplitter = None

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    if not text:
        return []
    if RecursiveCharacterTextSplitter:
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            return splitter.split_text(text)
        except Exception:
            pass
    chunks = []
    start = 0
    step = max(1, chunk_size - chunk_overlap)
    while start < len(text):
        chunks.append(text[start:start+chunk_size])
        start += step
    return chunks
