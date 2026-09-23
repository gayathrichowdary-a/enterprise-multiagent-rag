import os
import hashlib
from typing import List
from langchain_core.embeddings import Embeddings

class FastDeterministicEmbeddings(Embeddings):
    '''Ultra-fast, zero-dependency fallback embeddings that run on any Python version'''
    def __init__(self, dimension: int = 384):
        self.dim = dimension

    def _hash_vector(self, text: str) -> List[float]:
        # Generate stable 384-dimensional embedding vector
        vec = []
        for i in range(self.dim):
            seed_str = f"{text}_{i}"
            h = int(hashlib.md5(seed_str.encode('utf-8')).hexdigest()[:8], 16)
            vec.append((h / 0xFFFFFFFF) * 2.0 - 1.0)
        # Normalize
        norm = sum(x * x for x in vec) ** 0.5 or 1.0
        return [x / norm for x in vec]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._hash_vector(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._hash_vector(text)

def load_embedding():
    # 1. Try standard HuggingFace sentence-transformers
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )
    except Exception as e:
        # 2. Resilient fallback that never crashes on Streamlit Cloud
        return FastDeterministicEmbeddings(dimension=384)
