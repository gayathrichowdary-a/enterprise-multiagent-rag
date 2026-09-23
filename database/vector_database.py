import os

from rag.embeddings import load_embedding
from rag.vector_store import load_vector_db


def load_user_vectors(user_id):

    embedding = load_embedding()

    vector_stores = {}

    base_path = os.path.join(
        "vector_store",
        str(user_id)
    )

    if not os.path.exists(base_path):
        return vector_stores

    for folder in os.listdir(base_path):

        folder_path = os.path.join(
            base_path,
            folder
        )

        db = load_vector_db(
            folder_path,
            embedding
        )

        vector_stores[folder] = db

    return vector_stores