import streamlit as st

def history_page():

    st.title("📜 Chat History")

    chats = st.session_state.get("chats", {})

    if not chats:
        st.info("No conversations available.")
        return

    for chat_name, messages in chats.items():

        with st.expander(chat_name):

            if not messages:
                st.write("Empty conversation.")
                continue

            for msg in messages:

                st.markdown(f"**You:** {msg['query']}")
                st.markdown(f"**Assistant:** {msg['answer']}")
                st.divider()