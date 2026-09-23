# dashboard/upload.py
import streamlit as st
import os
import shutil
import hashlib
from pathlib import Path

from loaders.loader_router import load_document
from rag.chunker import chunk_text
from rag.embeddings import load_embedding
from rag.vector_store import create_vector_db

from langchain_community.vectorstores import FAISS

ALLOWED_FILE_TYPES = ["pdf", "docx", "txt", "png", "jpg", "jpeg"]
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
HASH_FILE_NAME = "source_hash.txt"


# ---------------------------------
# HELPERS
# ---------------------------------
def compute_file_hash(file_path):
    """Return SHA256 hash of a file's contents."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            sha256.update(block)
    return sha256.hexdigest()


def load_vector_db(vector_path, embedding):
    """Load an existing FAISS vector store from disk."""
    return FAISS.load_local(
        vector_path,
        embedding,
        allow_dangerous_deserialization=True,
    )


# ---------------------------------
# SIDEBAR
# ---------------------------------
def document_sidebar():
    st.subheader("📂 Loaded Documents")

    if st.session_state.vector_stores:
        for file_name, data in st.session_state.knowledge_sources.items():
            tier = data.get("authority_tier", "Tier 2")
            st.caption(f"📄 {file_name} • **{tier.split(' ')[0]}**")
    else:
        st.caption("No documents uploaded.")

    st.divider()

    if st.button(
        "📄 Clear Uploaded Documents",
        key="btn_clear_uploaded_docs",
        use_container_width=True,
    ):
        st.session_state.vector_stores = {}
        st.session_state.uploaded_documents = []
        st.session_state.knowledge_sources = {}

        user_id = st.session_state.get("user", {}).get("id", 1)

        upload_dir = os.path.join("uploads", str(user_id))
        if os.path.exists(upload_dir):
            shutil.rmtree(upload_dir)
        os.makedirs(upload_dir, exist_ok=True)

        vector_dir = os.path.join("vector_store", str(user_id))
        if os.path.exists(vector_dir):
            shutil.rmtree(vector_dir)
        os.makedirs(vector_dir, exist_ok=True)

        st.success("Uploaded documents cleared.")
        st.rerun()

    st.divider()
    st.info(
        "🔒 Enterprise Privacy Note\n\n"
        "Documents are indexed with Authority Tiers for Adaptive Multi-Agent Verification."
    )


# ---------------------------------
# MAIN PAGE
# ---------------------------------
def upload_page():
    st.title("📤 Enterprise Document Ingestion")
    st.caption("Upload documents and assign Enterprise Authority Tiers for Source Reliability Ranking.")

    # Enterprise Metadata Configuration
    col1, col2 = st.columns(2)
    with col1:
        department = st.selectbox(
            "🏢 Enterprise Department",
            [
                "Legal & InfoSec Compliance",
                "DevOps & Infrastructure (SRE)",
                "Software Engineering",
                "Human Resources (HR)",
                "Customer Operations",
                "General / Other"
            ]
        )
    with col2:
        authority_tier = st.selectbox(
            "🛡️ Source Authority Tier",
            [
                "Tier 1 (Authoritative Policy / Runbook)",
                "Tier 2 (Internal Wiki / Confluence)",
                "Tier 3 (Informal Chat / Working Draft)"
            ],
            help="Tier 1 documents receive highest reliability weighting during Multi-Agent retrieval."
        )

    uploaded_files = st.file_uploader(
        "Choose Knowledge Source files",
        type=ALLOWED_FILE_TYPES,
        accept_multiple_files=True,
        key="file_uploader_widget"
    )

    if uploaded_files:
        st.write(f"📁 Selected **{len(uploaded_files)}** file(s). Click below to process and index:")
        
        # Explicit Process Button with full progress handling
        if st.button("🚀 Ingest & Index Documents", type="primary", use_container_width=True):
            user_id = st.session_state.get("user", {}).get("id", 1)
            upload_dir = os.path.join("uploads", str(user_id))
            os.makedirs(upload_dir, exist_ok=True)
            
            with st.spinner("Loading embeddings model and indexing documents..."):
                embedding = load_embedding()

                for file in uploaded_files:
                    if file.size > MAX_FILE_SIZE_BYTES:
                        st.error(f"❌ {file.name} exceeds {MAX_FILE_SIZE_MB} MB limit.")
                        continue

                    safe_file_name = os.path.basename(file.name)
                    file_path = os.path.join(upload_dir, safe_file_name)

                    # Save uploaded file bytes to disk
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())

                    new_hash = compute_file_hash(file_path)
                    vector_path = os.path.join("vector_store", str(user_id), safe_file_name)
                    hash_file_path = os.path.join(vector_path, HASH_FILE_NAME)

                    # Baseline trust score by tier
                    init_score = 95.0 if "Tier 1" in authority_tier else 80.0 if "Tier 2" in authority_tier else 55.0

                    # Check cached index
                    if os.path.exists(vector_path) and os.path.exists(hash_file_path):
                        with open(hash_file_path, "r") as hf:
                            old_hash = hf.read().strip()

                        if old_hash == new_hash:
                            st.info(f"⚡ Loading pre-indexed vector store for: `{safe_file_name}`")
                            vector_db = load_vector_db(vector_path, embedding)

                            st.session_state.vector_stores[safe_file_name] = vector_db
                            st.session_state.knowledge_sources[safe_file_name] = {
                                "type": os.path.splitext(safe_file_name)[1],
                                "vector_db": vector_db,
                                "department": department,
                                "authority_tier": authority_tier,
                                "reliability_score": init_score,
                                "positive_feedback": 0,
                                "negative_feedback": 0
                            }
                            if safe_file_name not in st.session_state.uploaded_documents:
                                st.session_state.uploaded_documents.append(safe_file_name)
                            continue
                        else:
                            st.warning(f"♻️ Re-indexing updated file: `{safe_file_name}`...")
                            shutil.rmtree(vector_path)

                    # Load, chunk, and embed
                    documents = load_document(file_path)
                    chunks = chunk_text(documents)

                    for chunk in chunks:
                        chunk.metadata["source_name"] = safe_file_name
                        chunk.metadata["department"] = department
                        chunk.metadata["authority_tier"] = authority_tier

                    vector_db = create_vector_db(chunks, embedding)

                    os.makedirs(vector_path, exist_ok=True)
                    vector_db.save_local(vector_path)
                    with open(hash_file_path, "w") as hf:
                        hf.write(new_hash)

                    st.session_state.vector_stores[safe_file_name] = vector_db
                    st.session_state.knowledge_sources[safe_file_name] = {
                        "type": os.path.splitext(safe_file_name)[1],
                        "vector_db": vector_db,
                        "department": department,
                        "authority_tier": authority_tier,
                        "reliability_score": init_score,
                        "positive_feedback": 0,
                        "negative_feedback": 0
                    }

                    if safe_file_name not in st.session_state.uploaded_documents:
                        st.session_state.uploaded_documents.append(safe_file_name)

                st.success("✅ Successfully ingested and indexed documents into vector store!")
                st.rerun()

    # Display Active Sources Table
    if st.session_state.knowledge_sources:
        st.divider()
        st.subheader("📚 Active Enterprise Knowledge Sources")
        for name, data in st.session_state.knowledge_sources.items():
            st.write(f"📄 **{name}** | Dept: `{data.get('department', 'General')}` | Authority: `{data.get('authority_tier', 'Tier 2')}` | Reliability: `{data.get('reliability_score', 80.0)}%`")