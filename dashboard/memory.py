import streamlit as st
from database.memory_database import load_memory

def memory_page():
    st.title("🧠 Memory & Knowledge Base")
    st.caption("Centralized repository of document key aspects and long-term agent context.")

    user = st.session_state.get("user", {})
    if isinstance(user, dict):
        user_id = user.get("id") or user.get("user_id") or 1
    else:
        user_id = 1

    # 1. Document Key Aspects & Extracted Knowledge
    st.subheader("📚 Document Knowledge & Key Aspects")
    knowledge_sources = st.session_state.get("knowledge_sources", {})
    raw_texts = st.session_state.get("raw_document_texts", {})
    available_docs = list(knowledge_sources.keys()) or list(raw_texts.keys()) or st.session_state.get("uploaded_documents", [])

    if available_docs:
        for doc_name in available_docs:
            with st.expander(f"📄 {doc_name}", expanded=True):
                doc_data = knowledge_sources.get(doc_name, {})
                if isinstance(doc_data, dict) and doc_data.get("summary"):
                    st.markdown("**📌 Key Summary:**")
                    st.write(doc_data.get("summary"))
                elif doc_name in raw_texts:
                    preview_text = str(raw_texts[doc_name])[:500]
                    st.markdown("**📌 Knowledge Preview:**")
                    st.write(preview_text + ("..." if len(str(raw_texts[doc_name])) > 500 else ""))
                else:
                    st.info(f"Knowledge from `{doc_name}` is vectorized and active in memory.")
    else:
        st.info("📄 No documents processed yet. Upload documents in **📤 Upload Documents** to populate key aspects.")

    st.divider()

    # 2. Stored Context & Learned Agent Facts
    st.subheader("💡 Learned Facts & Long-term Context")
    try:
        memories = load_memory(user_id)
    except Exception:
        memories = []

    if memories:
        for memory in memories:
            mem_text = memory.get("fact") if isinstance(memory, dict) else str(memory)
            st.success(f"📌 {mem_text}")
    else:
        st.info("💡 No custom learned facts stored yet. As you converse in Chat and ask queries, key facts and preferences will be recorded here.")
