import datetime
import uuid
import streamlit as st


def log_query(query, answer, sources, trace, files):
    """Save one chat question (newest first)."""
    hist = st.session_state.setdefault("query_history", [])
    hist.insert(0, {
        "id": uuid.uuid4().hex[:8],
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "query": query,
        "answer": answer,
        "sources": sources,
        "trace": trace,
        "files": list(files or []),
    })


def open_in_chat(entry):
    """Reopen a past question and its answer in the Chat page."""
    st.session_state["chat_messages"] = [
        {"role": "user", "content": entry["query"]},
        {
            "role": "assistant",
            "content": entry["answer"],
            "sources": entry.get("sources", []),
            "trace": entry.get("trace", {}),
        },
    ]
    st.session_state["restore_files"] = entry.get("files", [])
    st.session_state["page"] = "dashboard"
    st.session_state["nav_selection"] = "Chat"
    st.rerun()