import streamlit as st
from dashboard.history_store import open_in_chat


def history_page():
    col_t, col_b = st.columns([5, 1])
    with col_t:
        st.title("📜 Query History")
        st.caption("Questions you asked in Chat. Click one to reopen it in the chat.")
    with col_b:
        st.write("")
        if st.button("💬 Chat Console", key="hist_to_chat", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.session_state["nav_selection"] = "Chat"
            st.rerun()

    history = st.session_state.get("query_history", [])

    if not history:
        st.info("No questions yet. Ask something in Chat and it will appear here.")
        return

    c_search, c_clear = st.columns([5, 1])
    with c_search:
        term = st.text_input(
            "Search your questions",
            key="hist_search",
            placeholder="🔍 Search your questions...",
            label_visibility="collapsed",
        )
    with c_clear:
        if st.button("Clear all", key="hist_clear_all", use_container_width=True):
            st.session_state["query_history"] = []
            st.rerun()

    shown = [h for h in history if term.strip().lower() in h["query"].lower()]
    st.caption(f"{len(shown)} of {len(history)} questions")

    if not shown:
        st.warning("No questions match your search.")
        return

    for h in shown:
        c1, c2, c3 = st.columns([8, 2, 1])
        with c1:
            q = h["query"]
            label = q if len(q) <= 110 else q[:107] + "..."
            if st.button(f"💬 {label}", key=f"hist_open_{h['id']}", use_container_width=True):
                open_in_chat(h)
        with c2:
            st.caption(h["time"])
        with c3:
            if st.button("🗑️", key=f"hist_del_{h['id']}", help="Delete this question"):
                st.session_state["query_history"] = [x for x in history if x["id"] != h["id"]]
                st.rerun()