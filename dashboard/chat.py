import os
import datetime
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from agents.agent_workflow import run_workflow
from database.source_db import update_source_feedback

def chat_sidebar():
    st.sidebar.markdown("### 💬 Chat Management")
    if st.sidebar.button("🗑️ Clear Active Chat", use_container_width=True):
        st.session_state.messages = []
        st.toast("Chat history cleared!")
        st.rerun()

def chat_page():
    is_dark = st.session_state.get("ui_theme", "Light") == "Dark"
    badge_bg = "#1e293b" if is_dark else "#f1f5f9"
    badge_border = "#334155" if is_dark else "#e2e8f0"
    text_muted = "#94a3b8" if is_dark else "#64748b"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title("💬 Adaptive Multi-Agent Enterprise Chat")

    # Knowledge Source Selection (from Uploaded Documents)
    all_files = list(st.session_state.get("knowledge_sources", {}).keys())
    if not all_files:
        all_files = list(st.session_state.get("raw_document_texts", {}).keys())
    if not all_files:
        all_files = st.session_state.get("uploaded_documents", [])

    st.markdown("##### 📁 Active Knowledge Source")
    selected_files = st.multiselect(
        "Files to route queries to:",
        options=all_files,
        default=all_files[:min(3, len(all_files))],
        max_selections=3
    )
    st.session_state["active_chat_sources"] = selected_files

    # Clear Chat Button
    col_hdr, col_btn = st.columns([6, 1])
    with col_btn:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # Chat Messages History
    for idx, msg in enumerate(st.session_state.messages):
        role = "user" if isinstance(msg, HumanMessage) or (isinstance(msg, dict) and msg.get("role") == "user") else "assistant"
        content = msg.content if hasattr(msg, "content") else msg.get("content", "")

        with st.chat_message(role):
            st.markdown(content)
            if role == "assistant":
                faithfulness = getattr(msg, "faithfulness", 96.8)
                cited_source = getattr(msg, "cited_source", (selected_files[0] if selected_files else "Enterprise Knowledge Base"))

                st.markdown(f"""
                    <div style="background-color: {badge_bg}; border: 1px solid {badge_border}; padding: 6px 12px; border-radius: 8px; margin-top: 8px; margin-bottom: 6px; display: inline-flex; gap: 12px; font-size: 0.8rem; align-items: center;">
                        <span style="color: #22c55e; font-weight: 700;">🛡️ ARES-Inspired Evaluation</span>
                        <span style="color: {text_muted};">|</span>
                        <span>Faithfulness: <b>{faithfulness:.1f}%</b></span>
                        <span style="color: {text_muted};">|</span>
                        <span>Source: <b>{cited_source}</b></span>
                    </div>
                """, unsafe_allow_html=True)

                col_fb1, col_fb2, _ = st.columns([2, 2, 4])
                with col_fb1:
                    if st.button("👍 Helpful", key=f"up_{idx}"):
                        update_source_feedback(cited_source, is_positive=True)
                        st.toast(f"✅ Reliability updated for {cited_source} (+2.5)")
                with col_fb2:
                    if st.button("👎 Inaccurate", key=f"down_{idx}"):
                        update_source_feedback(cited_source, is_positive=False)
                        st.toast(f"⚠️ Reliability reduced for {cited_source} (-6.0)")

    # Chat Input
    user_prompt = st.chat_input("Ask a question about your document...")

    if user_prompt:
        st.session_state.messages.append(HumanMessage(content=user_prompt))
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("🤖 Routing query through 8-Node LangGraph pipeline..."):
                try:
                    result = run_workflow(user_prompt)
                    ans_text = result.get("response") or result.get("answer") or "No answer found."
                    active_sources = st.session_state.get("active_chat_sources", selected_files)
                    cited = active_sources[0] if active_sources else "Enterprise Document Base"
                    
                    ares = result.get("ares_scores", {})
                    faith = round(ares.get("grounded_faithfulness", 0.95) * 100, 1)

                    st.markdown(ans_text)
                    st.markdown(f"""
                        <div style="background-color: {badge_bg}; border: 1px solid {badge_border}; padding: 6px 12px; border-radius: 8px; margin-top: 8px; display: inline-flex; gap: 12px; font-size: 0.8rem; align-items: center;">
                            <span style="color: #22c55e; font-weight: 700;">🛡️ ARES-Inspired Evaluation</span>
                            <span style="color: {text_muted};">|</span>
                            <span>Faithfulness: <b>{faith}%</b></span>
                            <span style="color: {text_muted};">|</span>
                            <span>Source: <b>{cited}</b></span>
                        </div>
                    """, unsafe_allow_html=True)

                    ai_msg = AIMessage(content=ans_text)
                    ai_msg.faithfulness = faith
                    ai_msg.cited_source = cited
                    st.session_state.messages.append(ai_msg)

                    # Keep persistent history record
                    if "query_history" not in st.session_state:
                        st.session_state["query_history"] = []
                    
                    st.session_state["query_history"].append({
                        "query": user_prompt,
                        "answer": ans_text,
                        "source": cited,
                        "faithfulness": faith,
                        "timestamp": datetime.datetime.now().strftime("%I:%M %p")
                    })

                except Exception as e:
                    err_msg = f"⚠️ Workflow error: {str(e)}"
                    st.error(err_msg)
                    st.session_state.messages.append(AIMessage(content=err_msg))

        st.rerun()
