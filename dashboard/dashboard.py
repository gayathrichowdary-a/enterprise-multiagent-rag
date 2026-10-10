import os
import base64
import time
import traceback
import streamlit as st

# Modular safe imports
try:
    from dashboard.nav import render_sidebar
except Exception:
    def render_sidebar(current_page="Chat"):
        pass

try:
    from dashboard.upload import document_sidebar, upload_page
except Exception:
    def document_sidebar():
        st.markdown("### 📁 Knowledge Base")
    def upload_page():
        st.info("Upload module initialized.")

try:
    from dashboard.chat import chat_sidebar
except Exception:
    def chat_sidebar():
        st.markdown("### 🤖 Multi-Agent Settings")

# Saves each question to the History page
try:
    from dashboard.history_store import log_query
except Exception:
    def log_query(query, answer, sources, trace, files):
        pass

# Real RAG workflow (errors are shown on the page, never hidden)
_WORKFLOW_ERR = None
try:
    from agents.agent_workflow import run_workflow
except Exception:
    run_workflow = None
    _WORKFLOW_ERR = traceback.format_exc()


def get_available_documents():
    """Documents that have real extracted text (newest first)."""
    raw = st.session_state.get("raw_document_texts", {})
    return [d["name"] for d in st.session_state.get("documents_list", []) if d.get("name") in raw]


def run_rag_pipeline(query, selected_files=None):
    """Run the real workflow on the selected documents."""
    if run_workflow is None:
        raise RuntimeError("Could not import agents.agent_workflow.run_workflow:\n" + (_WORKFLOW_ERR or ""))

    st.session_state["active_chat_sources"] = list(selected_files or [])
    res = run_workflow(query, selected_files=selected_files)

    if not isinstance(res, dict):
        return str(res), [], {}

    answer = res.get("answer") or res.get("response") or "No answer was returned by the workflow."

    docs_by_name = {d.get("name"): d for d in st.session_state.get("documents_list", [])}
    sources = []
    for name in res.get("sources", []):
        d = docs_by_name.get(name, {})
        rel = d.get("reliabilityScore")
        sources.append({
            "name": name,
            "tier": d.get("authorityTier", "Unclassified"),
            "reliability": f"{rel}%" if rel is not None else "n/a",
            "snippet": "",
        })

    trace = {"ares": res.get("ares_scores", {}) or {}}
    return answer, sources, trace


def get_dashboard_image_b64():
    """Retrieve base64 image string for dashboard robot across common asset paths."""
    possible_paths = [
        "assets/dashboard_robot.png",
        "assets/dashboard_robot.jpg",
        "assets/dashboard_robot.jpeg",
        "dashboard/dashboard_robot.png",
        "dashboard/dashboard_robot.jpg",
        "dashboard_robot.png",
        "dashboard_robot.jpg",
        "assets/login_robot.jpg",
        "assets/signup_robot.jpg",
    ]
    for p in possible_paths:
        if os.path.exists(p):
            try:
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                pass
    return None


def inject_global_theme(dark: bool = False):
    """Inject premium CSS styling matching enterprise UI standards."""
    bg_color = "#0B0F19" if dark else "#F8FAFC"
    card_bg = "#111827" if dark else "#FFFFFF"
    text_color = "#F3F4F6" if dark else "#1E293B"
    border_color = "rgba(255,255,255,0.08)" if dark else "rgba(0,0,0,0.06)"

    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        [data-testid="stSidebar"] {{
            background-color: {"#0D1322" if dark else "#FFFFFF"};
            border-right: 1px solid {border_color};
        }}
        .metric-card {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: transparent;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 10px;
            padding: 8px 18px;
            font-weight: 600;
        }}
        </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """Ensure all required session state variables exist."""
    if "dark_mode" not in st.session_state:
        st.session_state["dark_mode"] = False

    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": "👋 **Welcome to the Adaptive Enterprise RAG Platform!**\n\nUpload a document on the **Upload Documents** page, select it under **Active Knowledge Source**, and ask me anything about it.",
                "sources": [],
                "trace": {},
            }
        ]

    if "documents_list" not in st.session_state:
        from dashboard.upload import DEFAULT_SOURCES
        st.session_state["documents_list"] = [dict(s) for s in DEFAULT_SOURCES]

    if "total_docs" not in st.session_state:
        st.session_state["total_docs"] = len(st.session_state["documents_list"])

    if "vector_chunks" not in st.session_state:
        st.session_state["vector_chunks"] = sum(d["chunks"] for d in st.session_state["documents_list"])


def dashboard():
    """Main Dashboard view for Enterprise Multi-Agent RAG Platform."""
    init_session_state()

    # 1. Apply global theme
    is_dark = st.session_state.get("dark_mode", False)
    inject_global_theme(is_dark)

    # 2. Hero Welcome Card featuring the 3D Dashboard Robot
    img_b64 = get_dashboard_image_b64()
    img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width: 140px; height: 140px; object-fit: cover; border-radius: 18px; box-shadow: 0 10px 25px rgba(2, 18, 53, 0.4); border: 1px solid rgba(255, 255, 255, 0.15);" alt="Dashboard AI Robot" />' if img_b64 else '<div style="font-size: 64px;">🤖</div>'

    current_mode = st.session_state.get("agent_mode_select", "Adaptive Multi-Agent (Authority-Weighted)")
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #021235 0%, #031B4E 55%, #06286E 100%);
                    border-radius: 24px; padding: 26px 30px; color: #FFFFFF;
                    box-shadow: 0 20px 40px -15px rgba(2, 18, 53, 0.45);
                    border: 1px solid rgba(255, 255, 255, 0.12);
                    display: flex; align-items: center; justify-content: space-between;
                    margin-bottom: 2rem; gap: 24px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 260px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="background: #2563EB; color: white; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;">ADAPTIVE SYSTEM</span>
                    <span style="color: #38BDF8; font-size: 12px; font-weight: 600;">Mode: {current_mode}</span>
                </div>
                <h2 style="color: #FFFFFF; font-size: 26px; font-weight: 800; margin: 0 0 8px 0; line-height: 1.25;">
                    Adaptive Multi-Agent <span style="color: #38BDF8;">RAG & Source Reliability</span>
                </h2>
                <p style="color: #94A3B8; font-size: 14px; margin: 0 0 16px 0; line-height: 1.5; font-weight: 400;">
                    Autonomous routing, Tier-weighted source authority, ARES Tri-Judge quality assessment, and continuous feedback loop.
                </p>
                <div style="display: flex; gap: 12px; flex-wrap: wrap; font-size: 12px; color: #7DD3FC;">
                    <span>• Top-K: {st.session_state.get("top_k_slider", 4)} chunks</span>
                    <span>• Temp: {st.session_state.get("temp_slider", 0.20)}</span>
                    <span>• ARES Tri-Judge: Active</span>
                </div>
            </div>
            <div style="flex-shrink: 0; display: flex; justify-content: center; align-items: center;">
                {img_tag}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3. KPI Metric Cards (live values)
    docs = st.session_state.get("documents_list", [])
    n_docs = len(docs)
    n_chunks = st.session_state.get("vector_chunks", sum(d.get("chunks", 0) for d in docs))
    avg_rel = round(sum(d.get("reliabilityScore", 0) for d in docs) / n_docs, 1) if n_docs else 0
    available_docs = get_available_documents()

    last_gf = None
    for m in reversed(st.session_state["chat_messages"]):
        ares = (m.get("trace") or {}).get("ares") or {}
        if ares.get("grounded_faithfulness"):
            last_gf = ares["grounded_faithfulness"]
            break
    gf_text = f"{last_gf * 100:.1f}%" if last_gf is not None else "—"

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase;">Indexed Documents</div>
                <div style="font-size: 26px; font-weight: 800; color: #2563EB; margin: 6px 0 2px 0;">{n_docs} Active</div>
                <div style="font-size: 12px; color: #10B981; font-weight: 600;">{len(available_docs)} ready for chat</div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase;">ARES Faithfulness</div>
                <div style="font-size: 26px; font-weight: 800; color: #10B981; margin: 6px 0 2px 0;">{gf_text}</div>
                <div style="font-size: 12px; color: #10B981; font-weight: 600;">Last answer</div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase;">Source Reliability</div>
                <div style="font-size: 26px; font-weight: 800; color: #8B5CF6; margin: 6px 0 2px 0;">{avg_rel}%</div>
                <div style="font-size: 12px; color: #6366F1; font-weight: 600;">Authority-Weighted</div>
            </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase;">Vector Chunks</div>
                <div style="font-size: 26px; font-weight: 800; color: #F59E0B; margin: 6px 0 2px 0;">{n_chunks:,} Chunks</div>
                <div style="font-size: 12px; color: #64748B; font-weight: 600;">Estimated</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 4. Interactive Chat Console
    st.subheader("💬 Interactive Multi-Agent Chat Console")

    st.markdown("##### 📂 Active Knowledge Source")
    col_sel, col_clear = st.columns([5, 1])
    with col_sel:
        if available_docs:
            # Documents restored from the History page take priority
            restored = [f for f in (st.session_state.pop("restore_files", None) or []) if f in available_docs]
            if restored:
                st.session_state["active_files_select"] = restored

            if "active_files_select" in st.session_state:
                # Drop selections for documents that were deleted since
                st.session_state["active_files_select"] = [
                    f for f in st.session_state["active_files_select"] if f in available_docs
                ]
                selected_files = st.multiselect(
                    "Files to route queries to:",
                    options=available_docs,
                    key="active_files_select",
                )
            else:
                selected_files = st.multiselect(
                    "Files to route queries to:",
                    options=available_docs,
                    default=available_docs[:1],
                    key="active_files_select",
                )
        else:
            selected_files = []
            st.info("No readable documents yet. Go to **Upload Documents**, upload a file and click **Index Staged Files Now**.")
    with col_clear:
        st.write("")
        if st.button("🗑️ Clear Chat", key="main_clear_chat_btn", use_container_width=True):
            st.session_state["chat_messages"] = []
            st.rerun()

    for msg in st.session_state["chat_messages"]:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg["content"])
                if msg.get("sources"):
                    with st.expander("📚 Source documents", expanded=False):
                        for s in msg["sources"]:
                            st.markdown(f"**[{s.get('tier', 'Unclassified')}] {s.get('name')}** (Reliability: {s.get('reliability', 'n/a')})")
                            if s.get("snippet"):
                                st.caption(f"> {s['snippet']}")
                ares = (msg.get("trace") or {}).get("ares") or {}
                if ares:
                    st.caption(
                        "🛡️ ARES-inspired (heuristic) — "
                        f"Context: {ares.get('context_relevance', 0) * 100:.0f}% | "
                        f"Faithfulness: {ares.get('grounded_faithfulness', 0) * 100:.0f}% | "
                        f"Answer: {ares.get('answer_relevance', 0) * 100:.0f}%"
                    )

    # Query input (also accepts the sidebar quick-prompt buttons)
    user_query = st.chat_input("Ask a question about your selected documents...") or st.session_state.pop("pending_query", None)
    if user_query:
        if not selected_files:
            st.warning("Select at least one document in 'Active Knowledge Source' first.")
            st.stop()

        st.session_state["chat_messages"].append({"role": "user", "content": user_query})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_query)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Autonomous Agent Orchestrating & ARES Filtering..."):
                try:
                    response_text, sources, trace = run_rag_pipeline(user_query, selected_files)
                except Exception:
                    st.error("The RAG pipeline failed. Full error below:")
                    st.code(traceback.format_exc())
                    st.stop()
                st.markdown(response_text)
                st.session_state["chat_messages"].append({
                    "role": "assistant",
                    "content": response_text,
                    "sources": sources,
                    "trace": trace,
                })
                log_query(user_query, response_text, sources, trace, selected_files)
        st.rerun()


render_chat = dashboard
__all__ = ["dashboard", "render_chat", "inject_global_theme"]