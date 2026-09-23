class InMemoryStore:
    def __init__(self, texts, metadatas=None):
        self.texts = texts
        self.metadatas = metadatas or [{} for _ in texts]
    def similarity_search(self, query, k=4):
        class Hit:
            def __init__(self, t, m):
                self.page_content = t
                self.metadata = m
        return [Hit(t, m) for t, m in zip(self.texts[:k], self.metadatas[:k])]
    def as_retriever(self, **kwargs):
        return self
    def get_relevant_documents(self, query):
        return self.similarity_search(query)

def create_vector_db(chunks, metadatas=None):
    try:
        from langchain_community.vectorstores import FAISS
        from rag.embedder import get_embeddings
        emb = get_embeddings()
        if metadatas:
            return FAISS.from_texts(texts=chunks, embedding=emb, metadatas=metadatas)
        return FAISS.from_texts(texts=chunks, embedding=emb)
    except Exception:
        return InMemoryStore(chunks, metadatas)

create_vector_store = create_vector_db
