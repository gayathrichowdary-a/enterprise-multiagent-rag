import streamlit as st
from database.memory_database import load_memory

def memory_page():
    st.title("🧠 Memory")
    
    # Safely extract user_id without KeyError
    user = st.session_state.get("user", {})
    if isinstance(user, dict):
        user_id = user.get("id") or user.get("user_id") or 1
    else:
        user_id = 1

    try:
        memories = load_memory(user_id)
    except Exception:
        memories = []

    if not memories:
        st.info("💡 No memories stored yet. As you converse in Chat, key facts and preferences will be recorded here.")
        return

    st.subheader("Stored Context & Key Learnings")
    for memory in memories:
        st.success(memory)
