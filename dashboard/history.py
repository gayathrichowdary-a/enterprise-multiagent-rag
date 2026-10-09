import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

def history_page():
    st.title("📜 Query History")
    st.caption("Click any question below to immediately open it and view the answer in Chat.")

    history_list = st.session_state.get("query_history", [])

    # Support legacy 'chats' dictionary from older runs
    if not history_list:
        legacy_chats = st.session_state.get("chats", {})
        if legacy_chats:
            for chat_name, messages in legacy_chats.items():
                if isinstance(messages, list):
                    for msg in messages:
                        if isinstance(msg, dict):
                            history_list.append({
                                "query": msg.get("query", "Previous Question"),
                                "answer": msg.get("answer", "No answer recorded."),
                                "source": msg.get("source", "Knowledge Base"),
                                "faithfulness": msg.get("faithfulness", 95.0),
                                "timestamp": msg.get("timestamp", "Recent")
                            })

    if not history_list:
        st.info("💡 No search queries yet. Ask questions in the 💬 Chat tab and they will appear here.")
        return

    st.markdown("### 🔍 Recent Queries")

    # Display newest first
    for idx, item in enumerate(reversed(history_list)):
        query_text = item.get("query", "Untitled Query")
        ans_text = item.get("answer", "")
        timestamp = item.get("timestamp", "")
        source = item.get("source", "Knowledge Base")
        faith = item.get("faithfulness", 95.0)

        col_q, col_btn = st.columns([6, 1.5])

        with col_q:
            st.markdown(f"**❓ {query_text}**")
            meta = []
            if timestamp:
                meta.append(f"🕒 {timestamp}")
            meta.append(f"📁 {source}")
            meta.append(f"🛡️ {faith}%")
            st.caption(" | ".join(meta))

        with col_btn:
            if st.button("💬 View in Chat", key=f"hist_btn_{idx}", use_container_width=True):
                h_msg = HumanMessage(content=query_text)
                a_msg = AIMessage(content=ans_text)
                a_msg.faithfulness = faith
                a_msg.cited_source = source

                st.session_state.messages = [h_msg, a_msg]
                st.session_state["nav_page"] = "💬 Chat"
                st.rerun()

        st.divider()
