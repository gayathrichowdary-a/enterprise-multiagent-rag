from langchain_community.embeddings import HuggingFaceEmbeddings

def load_embedding():

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embedding