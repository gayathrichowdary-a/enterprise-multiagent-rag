import streamlit as st

def settings_page():
    """Enterprise RAG Platform Settings & Configurations."""
    from dashboard.nav import render_sidebar
    render_sidebar("Settings")

    col_nav1, col_nav2 = st.columns([5, 1])
    with col_nav1:
        st.title("⚙️ Platform & Model Settings")
        st.caption("Configure agent execution pipelines, LLM routing thresholds, and vector DB credentials.")
    with col_nav2:
        if st.button("💬 Chat Console", key="btn_set_to_chat", use_container_width=True):
            st.session_state["nav_selection"] = "Chat"
            st.session_state["page"] = "dashboard"
            st.rerun()

    st.markdown("---")

    # Tabbed Settings
    tab_llm, tab_vector, tab_ares, tab_sec = st.tabs([
        "🤖 LLM & Agent Router",
        "🗄️ Vector Database & Embeddings",
        "📊 ARES Tri-Judge Calibration",
        "🔐 Security & Compliance"
    ])

    with tab_llm:
        st.markdown("#### Primary LLM & Agent Configuration")
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Primary Reasoning Model", [
                "Gemini 2.5 Flash (Recommended - Fast & Cost-Effective)",
                "Gemini 1.5 Pro (Deep Multi-Agent Reasoning)",
                "Claude 3.5 Sonnet",
                "GPT-4o (Enterprise)"
            ], index=0)
            st.slider("Agent Temperature", 0.0, 1.0, 0.2, 0.05, help="Lower values produce more deterministic responses.")
            st.slider("Max Output Tokens", 512, 8192, 2048, 256)
        with c2:
            st.selectbox("Agent Routing Mode", [
                "Adaptive Multi-Agent (Dynamic Fallback & Decomposition)",
                "Hybrid Dense + Sparse (RRF)",
                "Direct Dense Vector (Fast)",
                "Rule-Based Deterministic Only"
            ], index=0)
            st.slider("Routing Confidence Gate (%)", 50, 99, 85, 1)
            st.checkbox("Enable Multi-Agent Chain-of-Thought (CoT)", value=True)

    with tab_vector:
        st.markdown("#### Vector Engine & Embedding Pipeline")
        v1, v2 = st.columns(2)
        with v1:
            st.selectbox("Vector Database Backend", [
                "pgvector HNSW (Cloud SQL PostgreSQL)",
                "Pinecone Serverless (Cosine Metric)",
                "ChromaDB In-Memory (Dev)",
                "Milvus / Qdrant Enterprise"
            ], index=0)
            st.selectbox("Embedding Architecture", [
                "text-embedding-004 (768 dimensions)",
                "text-embedding-3-large (1536 dimensions)",
                "bge-large-en-v1.5 (1024 dimensions)"
            ], index=0)
        with v2:
            st.slider("Default Chunk Size (Tokens)", 128, 2048, 512, 64)
            st.slider("Default Chunk Overlap (Tokens)", 0, 256, 64, 16)
            st.slider("Top-K Retrieved Context Chunks", 1, 20, 5, 1)

    with tab_ares:
        st.markdown("#### ARES Automated Tri-Judge Metrics")
        st.caption("Calibrate synthetic PPI thresholds (Context Relevance, Answer Faithfulness, Answer Relevance).")
        a1, a2, a3 = st.columns(3)
        with a1:
            st.number_input("Context Relevance (CR) Min Gate", 0.0, 1.0, 0.70, 0.05)
        with a2:
            st.number_input("Answer Faithfulness (AF) Min Gate", 0.0, 1.0, 0.85, 0.05)
        with a3:
            st.number_input("Answer Relevance (AR) Min Gate", 0.0, 1.0, 0.80, 0.05)
        st.checkbox("Reject generation if Answer Faithfulness falls below threshold", value=True)

    with tab_sec:
        st.markdown("#### Security & Access Control")
        st.text_input("Tenant Isolation Key", value="tenant-enterprise-nmrec-prod", disabled=True)
        st.checkbox("Enforce Document RBAC / Role-based Filter", value=True)
        st.checkbox("PII Masking & Anonymization in Context", value=True)
        st.checkbox("Audit Log Every Query & Agent Execution Trace", value=True)

    st.markdown("---")
    if st.button("💾 Save Platform Configurations", type="primary"):
        st.toast("Settings updated successfully!")

__all__ = ["settings_page"]
