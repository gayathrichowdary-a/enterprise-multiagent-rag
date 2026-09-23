import streamlit as st

from database.memory_database import load_memory


def memory_page():

    st.title("🧠 Memory")

    user_id = st.session_state["user"]["id"]

    memories = load_memory(user_id)

    if not memories:

        st.info("No memories yet.")

        return

    for memory in memories:

        st.success(memory)