import streamlit as st
import json

def chat_sidebar():
    """Sidebar section for multi-agent RAG routing, retrieval parameters, and chat controls."""
    st.markdown("### 🤖 Multi-Agent Settings")

    # 1. Agent Routing Mode
    agent_mode = st.selectbox(
        "Agent Routing Mode",
        [
            "Autonomous Multi-Agent",
            "Hybrid RAG (BM25 + Dense)",
            "Strict Vector Semantic",
            "Deep Reasoning Agent",
            "Direct LLM (Bypass RAG)"
        ],
        index=0,
        key="agent_mode_select",
        help="Select which agent orchestration strategy handles incoming user queries."
    )

    # 2. Retrieval Hyperparameters
    top_k = st.slider(
        "Top-K Chunks to Retrieve",
        min_value=1,
        max_value=15,
        value=st.session_state.get("top_k_slider", 4),
        key="top_k_slider",
        help="Number of most relevant passage chunks passed to the reranker and generator."
    )

    rerank_threshold = st.slider(
        "Re-ranker Threshold",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.get("rerank_thresh_slider", 0.70),
        step=0.05,
        key="rerank_thresh_slider",
        help="Chunks scoring below this cross-encoder threshold are dropped to prevent hallucination."
    )

    temperature = st.slider(
        "Synthesis Temperature",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.get("temp_slider", 0.20),
        step=0.05,
        key="temp_slider",
        help="Lower values yield strict factual grounding; higher values yield more creative prose."
    )

    with st.expander("🔬 Advanced Search Parameters", expanded=False):
        st.selectbox(
            "Similarity Metric",
            ["Cosine Distance (1 - cos)", "Inner Dot Product", "L2 Euclidean Distance"],
            key="similarity_metric_select"
        )
        st.checkbox("Enable Reciprocal Rank Fusion (RRF)", value=True, key="enable_rrf_check")
        st.checkbox("Enforce Hallucination Verification Guard", value=True, key="enable_guard_check")

    # 3. Quick Test Query Prompts
    st.markdown("---")
    st.markdown("##### 💡 Sidebar Prompts")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("🔐 Security", key="sb_prompt_sec", use_container_width=True):
            st.session_state["pending_query"] = "What are the SOC2 security protocols and vector encryption methods?"
            st.rerun()
    with col_p2:
        if st.button("🏛️ Arch Spec", key="sb_prompt_arch", use_container_width=True):
            st.session_state["pending_query"] = "Explain the multi-agent RAG architecture and retrieval steps"
            st.rerun()

    # 4. Agent Fleet Status Display
    st.markdown("---")
    st.markdown("##### 🟢 Active Agent Fleet")
    st.caption("• **Router Agent:** Active (Intent Classifier)")
    st.caption("• **Dense Vector Agent:** Active (Cosine HNSW)")
    st.caption("• **Sparse BM25 Agent:** Active (Lexical Inverted)")
    st.caption("• **Cross-Encoder Reranker:** Active (MiniLM-L6)")

    # 5. Conversation Utilities
    st.markdown("---")
    messages = st.session_state.get("messages", [])

    if messages:
        chat_json_str = json.dumps(messages, indent=2)
        st.download_button(
            label="📥 Export Chat (JSON)",
            data=chat_json_str,
            file_name="rag_chat_history.json",
            mime="application/json",
            key="btn_export_chat",
            use_container_width=True
        )

    if st.button("🗑️ Clear Chat History", key="clear_chat_history_btn", use_container_width=True):
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "👋 Chat reset! Ready for your new queries across enterprise documents.",
                "agent_trace": {
                    "router": "System Reset Agent",
                    "retrieval": "Cleared Cache",
                    "confidence": "100%",
                },
                "sources": []
            }
        ]
        st.toast("Chat history cleared!")
        st.rerun()