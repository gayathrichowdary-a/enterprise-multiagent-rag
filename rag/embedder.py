try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
except ImportError:
    try:
        from langchain.embeddings import HuggingFaceEmbeddings
    except ImportError:
        HuggingFaceEmbeddings = None

def get_embeddings():
    if HuggingFaceEmbeddings:
        try:
            return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        except Exception:
            pass
    # Lightweight deterministic fallback
    class SimpleEmbeddings:
        def embed_documents(self, texts):
            return [[0.1] * 384 for _ in texts]
        def embed_query(self, text):
            return [0.1] * 384
    return SimpleEmbeddings()
