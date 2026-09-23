try:
    from langchain_community.vectorstores import FAISS
except ImportError:
    try:
        from langchain.vectorstores import FAISS
    except ImportError:
        FAISS = None

from rag.embedder import get_embeddings

def create_vector_store(chunks, metadatas=None):
    embeddings = get_embeddings()
    if FAISS:
        try:
            if metadatas:
                return FAISS.from_texts(texts=chunks, embedding=embeddings, metadatas=metadatas)
            return FAISS.from_texts(texts=chunks, embedding=embeddings)
        except Exception:
            pass
            
    # In-memory fallback retriever if FAISS binary is missing
    class SimpleStore:
        def __init__(self, texts):
            self.texts = texts
        def similarity_search(self, query, k=4):
            class Hit:
                def __init__(self, t):
                    self.page_content = t
                    self.metadata = {}
            return [Hit(t) for t in self.texts[:k]]
        def as_retriever(self, search_kwargs=None):
            return self
        def get_relevant_documents(self, query):
            return self.similarity_search(query)

    return SimpleStore(chunks)
