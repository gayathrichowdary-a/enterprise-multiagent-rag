import streamlit as st
import datetime
import random
from dashboard.indexer import index_files

# Initial enterprise source definitions for authority assignment
DEFAULT_SOURCES = [
    {
        "id": "src-1",
        "name": "Enterprise Security & Compliance Manual v4.2.pdf",
        "department": "Legal & InfoSec",
        "authorityTier": "Tier 1 (Authoritative)",
        "reliabilityScore": 98,
        "historicalQueries": 142,
        "positiveFeedback": 139,
        "negativeFeedback": 3,
        "chunks": 142,
        "size": "450 KB",
        "status": "Indexed",
        "trustStatus": "Certified",
        "updated": "2026-08-15"
    },
    {
        "id": "src-2",
        "name": "SRE Production Incident Response & On-Call Runbook.pdf",
        "department": "DevOps & Infrastructure",
        "authorityTier": "Tier 1 (Authoritative)",
        "reliabilityScore": 94,
        "historicalQueries": 198,
        "positiveFeedback": 188,
        "negativeFeedback": 10,
        "chunks": 98,
        "size": "320 KB",
        "status": "Indexed",
        "trustStatus": "Certified",
        "updated": "2026-09-02"
    },
    {
        "id": "src-3",
        "name": "Engineering Confluence: Cloud Migration & Architecture.md",
        "department": "Software Engineering",
        "authorityTier": "Tier 2 (Internal Verified)",
        "reliabilityScore": 86,
        "historicalQueries": 87,
        "positiveFeedback": 76,
        "negativeFeedback": 11,
        "chunks": 64,
        "size": "128 KB",
        "status": "Indexed",
        "trustStatus": "Certified",
        "updated": "2026-07-20"
    },
    {
        "id": "src-4",
        "name": "Global HR Benefits, Remote Work & Expense Policy 2026.docx",
        "department": "Human Resources",
        "authorityTier": "Tier 1 (Authoritative)",
        "reliabilityScore": 96,
        "historicalQueries": 115,
        "positiveFeedback": 111,
        "negativeFeedback": 4,
        "chunks": 315,
        "size": "890 KB",
        "status": "Indexed",
        "trustStatus": "Certified",
        "updated": "2026-06-10"
    },
    {
        "id": "src-5",
        "name": "Slack #dev-infra Archived Discussions & Notes.txt",
        "department": "Engineering Community",
        "authorityTier": "Tier 3 (Informal / Draft)",
        "reliabilityScore": 52,
        "historicalQueries": 45,
        "positiveFeedback": 24,
        "negativeFeedback": 21,
        "chunks": 54,
        "size": "78 KB",
        "status": "Indexed",
        "trustStatus": "Flagged",
        "updated": "2026-09-18"
    },
    {
        "id": "src-6",
        "name": "Customer Support Escalation Tier & SLA Guidelines.csv",
        "department": "Customer Operations",
        "authorityTier": "Tier 2 (Internal Verified)",
        "reliabilityScore": 89,
        "historicalQueries": 63,
        "positiveFeedback": 57,
        "negativeFeedback": 6,
        "chunks": 112,
        "size": "210 KB",
        "status": "Indexed",
        "trustStatus": "Certified",
        "updated": "2026-05-30"
    }
]


def init_knowledge_base_state():
    """Ensure documents and sources state is properly initialized."""
    if "documents_list" not in st.session_state or not st.session_state["documents_list"]:
        st.session_state["documents_list"] = [dict(s) for s in DEFAULT_SOURCES]

    if "total_docs" not in st.session_state:
        st.session_state["total_docs"] = len(st.session_state["documents_list"])

    if "vector_chunks" not in st.session_state:
        st.session_state["vector_chunks"] = sum(d["chunks"] for d in st.session_state["documents_list"])


def document_sidebar():
    """Sidebar section for document upload and knowledge base management."""
    init_knowledge_base_state()

    st.markdown("### 📁 Knowledge Base & Ingestion")

    # 1. Authority Tier selection for staged uploads
    upload_tier = st.selectbox(
        "Source Authority Tier",
        [
            "Tier 1 (Authoritative / Regulatory)",
            "Tier 2 (Internal Verified / Runbooks)",
            "Tier 3 (Informal / Slack / Field Notes)"
        ],
        index=0,
        key="sb_upload_tier",
        help="Tier 1 receives highest weighting in the retrieval reranker."
    )

    upload_dept = st.selectbox(
        "Department Tag",
        ["Legal & InfoSec", "DevOps & Infrastructure", "Software Engineering", "Human Resources", "Customer Operations"],
        index=0,
        key="sb_upload_dept"
    )

    # 2. File uploader for enterprise documents
    uploaded_files = st.file_uploader(
        "Upload Enterprise Documents",
        type=["pdf", "docx", "txt", "csv", "md", "json"],
        accept_multiple_files=True,
        help="Upload PDF, DOCX, TXT, CSV, Markdown, or JSON files to index into vector database.",
        key=f"sidebar_doc_uploader_{st.session_state.get('sb_upload_nonce', 0)}"
    )

    if uploaded_files:
        st.success(f"✓ {len(uploaded_files)} file(s) staged for indexing")
        if st.button("⚡ Index Staged Files", key="btn_index_staged", type="primary", use_container_width=True):
            result = index_files(uploaded_files, upload_tier, upload_dept, st.session_state.get("chunk_size_slider", 512))
            if result["problems"]:
                st.warning("Could not read: " + " | ".join(result["problems"]))
            if result["new"] or result["updated"]:
                st.toast(f"🎉 Indexed {len(result['new'])} new and refreshed {len(result['updated'])} existing file(s).")
            if not result["problems"]:
                st.session_state["sb_upload_nonce"] = st.session_state.get("sb_upload_nonce", 0) + 1
                st.rerun()

    # 3. Document Summary
    doc_count = len(st.session_state.get("documents_list", []))
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.caption(f"**Indexed Docs:** {doc_count}")
    with col_s2:
        st.caption(f"**Total Chunks:** {st.session_state.get('vector_chunks', 1284)}")

    # 4. Chunking & Embedding Settings
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

    # 5. Quick Actions
    with st.expander("🛠️ Knowledge Base Actions", expanded=False):
        if st.button("📥 Load Sample Enterprise Corpus", key="btn_load_samples", use_container_width=True):
            st.session_state["documents_list"] = [dict(s) for s in DEFAULT_SOURCES]
            st.session_state["total_docs"] = len(DEFAULT_SOURCES)
            st.session_state["vector_chunks"] = sum(d["chunks"] for d in DEFAULT_SOURCES)
            st.toast("Restored default enterprise knowledge corpus!")
            st.rerun()

        if st.button("🗑️ Clear All Indexed Documents", key="btn_clear_docs", use_container_width=True):
            st.session_state["documents_list"] = []
            st.session_state["raw_document_texts"] = {}
            st.session_state["total_docs"] = 0
            st.session_state["vector_chunks"] = 0
            st.toast("Knowledge base cleared.")
            st.rerun()


def upload_page():
    """Full-page view for Enterprise Document Ingestion & Source Reliability Management."""
    init_knowledge_base_state()

    col_nav1, col_nav2 = st.columns([5, 1])
    with col_nav1:
        st.title("📁 Knowledge Base & Source Management")
        st.caption("Ingest enterprise documents, assign Source Authority Tiers, and monitor vector embeddings.")
    with col_nav2:
        if st.button("💬 Chat Console", key="btn_upload_to_dash", use_container_width=True, type="primary"):
            st.session_state["page"] = "dashboard"
            st.rerun()

    # KPI Statistics Row
    doc_list = st.session_state.get("documents_list", [])
    doc_count = len(doc_list)
    vector_chunks = st.session_state.get("vector_chunks", 1284)
    avg_rel = round(sum(d.get("reliabilityScore", 90) for d in doc_list) / max(1, doc_count), 1) if doc_list else 0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Indexed Docs", doc_count, delta="Enterprise Corpus")
    with m2:
        st.metric("Vector Chunks", vector_chunks, delta="pgvector HNSW")
    with m3:
        st.metric("Avg Source Reliability", f"{avg_rel}%", delta="Tier-Weighted")
    with m4:
        st.metric("Embedding Dimension", "768d", delta="text-embedding-004")

    st.markdown("---")

    tab_upload, tab_catalog, tab_tiers, tab_config = st.tabs([
        "📤 Ingest Documents",
        "📚 Knowledge Catalog",
        "🏆 Source Authority Tiers",
        "⚙️ Vector Settings"
    ])

    with tab_upload:
        st.markdown("#### Upload Documents & Assign Source Authority")
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            tier_choice = st.selectbox(
                "Select Source Authority Tier",
                [
                    "Tier 1 (Authoritative / Regulatory Policy)",
                    "Tier 2 (Internal Verified / Architecture & Runbooks)",
                    "Tier 3 (Informal / Field Notes & Chat Archives)"
                ],
                key="page_tier_choice"
            )
        with col_u2:
            dept_choice = st.selectbox(
                "Department / Domain",
                ["Legal & InfoSec", "DevOps & Infrastructure", "Software Engineering", "Human Resources", "Customer Operations"],
                key="page_dept_choice"
            )

        uploaded_files = st.file_uploader(
            "Select files to index into enterprise knowledge store",
            type=["pdf", "docx", "txt", "csv", "md", "json"],
            accept_multiple_files=True,
            key=f"page_upload_files_{st.session_state.get('upload_nonce', 0)}"
        )

        if uploaded_files:
            st.success(f"✓ {len(uploaded_files)} file(s) staged and ready for vectorization.")
            if st.button("⚡ Index Staged Files Now", key="btn_page_index_now", type="primary", use_container_width=True):
                result = index_files(uploaded_files, tier_choice, dept_choice, st.session_state.get("page_chunk_size", 512))
                if result["problems"]:
                    st.warning("Could not read: " + " | ".join(result["problems"]))
                if result["new"] or result["updated"]:
                    st.toast(f"🎉 Indexed {len(result['new'])} new and refreshed {len(result['updated'])} existing file(s).")
                if not result["problems"]:
                    st.session_state["upload_nonce"] = st.session_state.get("upload_nonce", 0) + 1
                    st.rerun()

    with tab_catalog:
        st.markdown("#### Indexed Knowledge Catalog & Chunks")
        if doc_list:
            raw_texts = st.session_state.get("raw_document_texts", {})
            for i, doc in enumerate(doc_list):
                col_d1, col_d2, col_d3, col_d4 = st.columns([4, 2, 2, 1])
                with col_d1:
                    st.markdown(f"**📄 {doc.get('name', 'Document')}**")
                    st.caption(f"Dept: {doc.get('department', 'General')} • {doc.get('authorityTier', 'Tier 2')}")
                with col_d2:
                    st.markdown(f"**{doc.get('chunks', 0)} chunks** ({doc.get('size', 'N/A')})")
                    st.caption(f"Updated: {doc.get('updated', 'Today')}")
                with col_d3:
                    rel = doc.get('reliabilityScore', 90)
                    st.markdown(f"Reliability: **{rel}%**")
                    status = doc.get('trustStatus', 'Certified')
                    if status == "Certified":
                        st.caption("🟢 Certified")
                    elif status == "Under Review":
                        st.caption("🟡 Under Review")
                    else:
                        st.caption("🔴 Flagged")
                    if doc.get("name") in raw_texts:
                        st.caption("💬 Ready for chat")
                with col_d4:
                    if st.button("🗑️", key=f"del_doc_page_{i}", help="Remove from index"):
                        removed = doc_list.pop(i)
                        st.session_state.get("raw_document_texts", {}).pop(removed.get("name"), None)
                        st.session_state["documents_list"] = doc_list
                        st.session_state["total_docs"] = len(doc_list)
                        st.session_state["vector_chunks"] = sum(d.get("chunks", 4) for d in doc_list)
                        st.toast("Removed document")
                        st.rerun()
                st.markdown("---")
        else:
            st.info("No documents currently indexed. Ingest enterprise files or restore the sample corpus.")

    with tab_tiers:
        st.markdown("#### Source Reliability & Tiered Hierarchy Breakdown")
        t1, t2, t3 = st.columns(3)
        with t1:
            st.markdown("""
                <div style="background: #f0fdf4; border: 1.5px solid #22c55e; border-radius: 12px; padding: 14px; margin-bottom: 10px;">
                    <h4 style="color: #15803d; margin: 0 0 6px 0;">Tier 1: Authoritative</h4>
                    <p style="font-size: 12px; color: #166534; margin: 0;">Official regulations, InfoSec policies, audited compliance specifications, and certified runbooks.</p>
                    <div style="margin-top: 8px; font-weight: 700; color: #15803d; font-size: 13px;">Weight Factor: 1.00</div>
                </div>
            """, unsafe_allow_html=True)
        with t2:
            st.markdown("""
                <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 12px; padding: 14px; margin-bottom: 10px;">
                    <h4 style="color: #1d4ed8; margin: 0 0 6px 0;">Tier 2: Internal Verified</h4>
                    <p style="font-size: 12px; color: #1e40af; margin: 0;">Engineering Confluence wikis, architectural proposals, customer SLAs, and approved technical guides.</p>
                    <div style="margin-top: 8px; font-weight: 700; color: #1d4ed8; font-size: 13px;">Weight Factor: 0.75</div>
                </div>
            """, unsafe_allow_html=True)
        with t3:
            st.markdown("""
                <div style="background: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 12px; padding: 14px; margin-bottom: 10px;">
                    <h4 style="color: #b45309; margin: 0 0 6px 0;">Tier 3: Informal / Draft</h4>
                    <p style="font-size: 12px; color: #92400e; margin: 0;">Slack channels, quick meeting scratchpads, draft notes, and unverified anecdotal troubleshooting tips.</p>
                    <div style="margin-top: 8px; font-weight: 700; color: #b45309; font-size: 13px;">Weight Factor: 0.40</div>
                </div>
            """, unsafe_allow_html=True)

    with tab_config:
        st.markdown("#### Vector Pipeline Hyperparameters")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.slider("Chunk Size (tokens)", min_value=128, max_value=2048, value=512, step=64, key="page_chunk_size")
            st.slider("Chunk Overlap (tokens)", min_value=0, max_value=256, value=64, step=16, key="page_chunk_overlap")
        with col_c2:
            st.selectbox("Embedding Model", [
                "text-embedding-004 (768d)",
                "text-embedding-3-large (1536d)",
                "bge-large-en-v1.5 (1024d)"
            ], key="page_emb_model")
            st.selectbox("Vector Database Backend", [
                "pgvector HNSW (Cloud SQL)",
                "Pinecone Serverless (Cosine)",
                "Chroma In-Memory"
            ], key="page_vector_backend")

        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button("📥 Load Sample Enterprise Corpus", key="btn_page_load_sample", use_container_width=True):
                st.session_state["documents_list"] = [dict(s) for s in DEFAULT_SOURCES]
                st.session_state["total_docs"] = len(DEFAULT_SOURCES)
                st.session_state["vector_chunks"] = sum(d["chunks"] for d in DEFAULT_SOURCES)
                st.toast("Loaded sample corpus!")
                st.rerun()
        with col_act2:
            if st.button("🗑️ Clear All Indexed Documents", key="btn_page_clear_corpus", use_container_width=True):
                st.session_state["documents_list"] = []
                st.session_state["raw_document_texts"] = {}
                st.session_state["total_docs"] = 0
                st.session_state["vector_chunks"] = 0
                st.toast("Corpus cleared.")
                st.rerun()

__all__ = ["document_sidebar", "upload_page"]