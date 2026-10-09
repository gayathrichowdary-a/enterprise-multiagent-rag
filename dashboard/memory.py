import streamlit as st

def memory_page():
    """Episodic and Semantic Long-Term Agent Memory Explorer."""
    from dashboard.nav import render_sidebar
    render_sidebar("Memory")

    col_nav1, col_nav2 = st.columns([5, 1])
    with col_nav1:
        st.title("🧠 Agent Memory & Context Store")
        st.caption("Manage episodic session memories, persistent user profiles, and learned context vectors.")
    with col_nav2:
        if st.button("💬 Chat Console", key="btn_mem_to_chat", use_container_width=True):
            st.session_state["nav_selection"] = "Chat"
            st.session_state["page"] = "dashboard"
            st.rerun()

    st.markdown("---")

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Episodic Memories", "34", delta="+Active Session")
    with m2:
        st.metric("Semantic Entities", "128", delta="Long-Term Store")
    with m3:
        st.metric("Memory TTL", "30 Days", delta="Auto-Prune")
    with m4:
        st.metric("Context Recall Rate", "99.1%", delta="+ARES Bench")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Memory Categories
    tab_episodic, tab_profile, tab_vector_mem = st.tabs([
        "🕒 Episodic Session Memories",
        "👤 User Profile & Preferences",
        "🧬 Vectorized Semantic Memories"
    ])

    with tab_episodic:
        st.markdown("#### Conversation Episodes & Short-Term Working Memory")
        memories = [
            {"Timestamp": "2026-10-09 10:14", "Agent": "Router Agent", "Summary": "User inquired about SOC2 compliance and vector database encryption requirements.", "Importance": "High"},
            {"Timestamp": "2026-10-09 09:42", "Agent": "Evaluator Agent", "Summary": "Confirmed ARES Faithfulness score of 97.4% on MultiAgent Orchestration Spec.", "Importance": "Medium"},
            {"Timestamp": "2026-10-08 17:21", "Agent": "Retriever Agent", "Summary": "Ingested 5 documents into pgvector index with 512-token chunk boundaries.", "Importance": "High"},
            {"Timestamp": "2026-10-08 14:05", "Agent": "Ranker Agent", "Summary": "Promoted Tier 1 Technical Spec sources by +15% weight after positive user feedback.", "Importance": "High"}
        ]
        st.dataframe(memories, use_container_width=True)

    with tab_profile:
        st.markdown("#### Learned User Profile & Enterprise Context")
        st.info("The agent retains user preferences across interactions to minimize repetitive explanations.")
        p1, p2 = st.columns(2)
        with p1:
            st.text_input("User Preferred Output Format", value="Executive bullet points + Source Citations")
            st.text_input("Technical Depth Preference", value="Senior Engineering / Architectural")
        with p2:
            st.text_input("Default Vector Distance Metric", value="Cosine Similarity (1 - distance)")
            st.text_input("Default Domain Scope", value="NMREC AI & Data Science Enterprise Corpus")

    with tab_vector_mem:
        st.markdown("#### Vector Memory Store (Embedding Space)")
        st.caption("Memories encoded as 768d vectors retrieved during contextual prompt compilation.")
        if st.button("🧹 Flush Expired Working Memories"):
            st.toast("Cleared 4 stale session memories.")

__all__ = ["memory_page"]
