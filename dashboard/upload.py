import streamlit as st
import datetime
import random

def document_sidebar():
    """Sidebar section for document upload and knowledge base management."""
    st.markdown("### 📁 Knowledge Base")

    # 1. File uploader for enterprise documents
    uploaded_files = st.file_uploader(
        "Upload Enterprise Documents",
        type=["pdf", "docx", "txt", "csv", "md", "json"],
        accept_multiple_files=True,
        help="Upload PDF, DOCX, TXT, CSV, Markdown, or JSON files to index into the vector database.",
        key="sidebar_doc_uploader"
    )

    if uploaded_files:
        st.success(f"✓ {len(uploaded_files)} file(s) staged for indexing")
        if st.button("⚡ Index Staged Files", key="btn_index_staged", type="primary", use_container_width=True):
            if "documents_list" not in st.session_state:
                st.session_state["documents_list"] = []

            today_str = datetime.date.today().strftime("%Y-%m-%d")
            chunk_size = st.session_state.get("chunk_size_slider", 512)
            
            added_chunks = 0
            for f in uploaded_files:
                file_size_kb = max(1, round(len(f.getvalue()) / 1024, 1)) if hasattr(f, 'getvalue') else 24
                calc_chunks = max(4, int(file_size_kb * 1024 / chunk_size))
                added_chunks += calc_chunks
                
                ext = f.name.split(".")[-1].lower()
                cat_map = {
                    "pdf": "Technical / Specification",
                    "docx": "Compliance & Policy",
                    "txt": "Internal Notes",
                    "csv": "Structured Analytics",
                    "md": "Engineering Docs",
                    "json": "Schema & API"
                }
                category = cat_map.get(ext, "Enterprise Corpus")

                existing_names = [d["name"] for d in st.session_state["documents_list"]]
                if f.name not in existing_names:
                    st.session_state["documents_list"].insert(0, {
                        "id": f"doc-{random.randint(100, 999)}",
                        "name": f.name,
                        "category": category,
                        "chunks": calc_chunks,
                        "size": f"{file_size_kb} KB",
                        "status": "Indexed",
                        "updated": today_str
                    })

            st.session_state["total_docs"] = len(st.session_state["documents_list"])
            st.session_state["vector_chunks"] = st.session_state.get("vector_chunks", 1284) + added_chunks
            st.toast(f"🎉 Successfully indexed {len(uploaded_files)} file(s) into {added_chunks} vector chunks!")
            st.rerun()

    # 2. Document Summary
    doc_count = len(st.session_state.get("documents_list", []))
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.caption(f"**Indexed Docs:** {doc_count}")
    with col_s2:
        st.caption(f"**Total Chunks:** {st.session_state.get('vector_chunks', 1284)}")

    # 3. Chunking & Embedding Parameters Expander
    with st.expander("⚙️ Chunking & Vector Settings", expanded=False):
        st.slider("Chunk Size (tokens)", min_value=128, max_value=2048, value=512, step=64, key="chunk_size_slider")
        st.slider("Chunk Overlap (tokens)", min_value=0, max_value=256, value=64, step=16, key="chunk_overlap_slider")
        st.selectbox("Embedding Model", [
            "text-embedding-004 (768d)",
            "text-embedding-3-large (1536d)",
            "bge-large-en-v1.5 (1024d)"
        ], key="emb_model_select")
        st.selectbox("Vector Index", [
            "pgvector HNSW (Cloud SQL)",
            "Pinecone Serverless (Cosine)",
            "Chroma In-Memory"
        ], key="vector_backend_select")

    # 4. Quick Actions
    with st.expander("🛠️ Knowledge Base Actions", expanded=False):
        if st.button("📥 Load Sample Enterprise Corpus", key="btn_load_samples", use_container_width=True):
            sample_docs = [
                {"id": "doc-01", "name": "Enterprise_Security_Architecture_v4.pdf", "category": "Security & SecOps", "chunks": 142, "size": "450 KB", "status": "Indexed", "updated": "2026-10-08"},
                {"id": "doc-02", "name": "MultiAgent_Orchestration_Spec.pdf", "category": "Engineering", "chunks": 98, "size": "320 KB", "status": "Indexed", "updated": "2026-10-07"},
                {"id": "doc-03", "name": "Global_Compliance_SOC2_HIPAA.docx", "category": "Legal & Audit", "chunks": 315, "size": "890 KB", "status": "Indexed", "updated": "2026-10-06"},
                {"id": "doc-04", "name": "Hybrid_Vector_Retrieval_Benchmark.md", "category": "AI Research", "chunks": 64, "size": "128 KB", "status": "Indexed", "updated": "2026-10-05"},
                {"id": "doc-05", "name": "Q3_Infrastructure_SLA_CostReport.csv", "category": "DevOps", "chunks": 112, "size": "210 KB", "status": "Indexed", "updated": "2026-10-04"},
            ]
            st.session_state["documents_list"] = sample_docs
            st.session_state["total_docs"] = len(sample_docs)
            st.session_state["vector_chunks"] = sum(d["chunks"] for d in sample_docs)
            st.toast("Restored default enterprise knowledge corpus!")
            st.rerun()

        if st.button("🗑️ Clear All Indexed Documents", key="btn_clear_docs", use_container_width=True):
            st.session_state["documents_list"] = []
            st.session_state["total_docs"] = 0
            st.session_state["vector_chunks"] = 0
            st.toast("Knowledge base cleared.")
            st.rerun()