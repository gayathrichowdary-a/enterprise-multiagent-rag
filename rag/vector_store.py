import os
from langchain_community.vectorstores import FAISS

def create_vector_db(chunks, embedding):
    """
    Creates a new FAISS vector database from text chunks and embedding model.
    """
    if not chunks:
        return None
    return FAISS.from_documents(chunks, embedding)

def load_vector_db(vector_path, embedding):
    """
    Loads an existing FAISS vector store from disk.
    """
    if not os.path.exists(vector_path):
        return None
    return FAISS.load_local(
        vector_path,
        embedding,
        allow_dangerous_deserialization=True
    )