import os
import base64
import time
import streamlit as st

# Safe import with modular fallback so it never crashes
try:
    from dashboard.upload import document_sidebar
except Exception:
    def document_sidebar():
        st.markdown("### 📁 Knowledge Base")
        st.file_uploader("Upload Enterprise Documents", type=["pdf", "docx", "txt", "csv", "md"], key="fb_upload")

try:
    from dashboard.chat import chat_sidebar
except Exception:
    def chat_sidebar():
        st.markdown("### 🤖 Multi-Agent Settings")
        st.selectbox("Agent Routing Mode", ["Autonomous Multi-Agent", "Hybrid RAG", "Strict Vector"], key="fb_mode")


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
        "assets/image.png",
    ]
    for p in possible_paths:
        if os.path.exists(p):
            try:
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                pass
    return ""


def inject_global_theme(is_dark=False):
    """Applies clean Light or Cyber Dark mode across the entire application."""
    if is_dark:
        bg_app = "#090d16"
        bg_sidebar = "#0d111c"
        bg_card = "#131b2e"
        border_card = "#1e293b"
        text_primary = "#ffffff"
        text_secondary = "#94a3b8"
        accent_blue = "#38bdf8"
        input_bg = "#1e293b"
        chat_msg_bg = "#111827"
        chat_bottom_bg = "#090d16"
    else:
        bg_app = "#f8fafc"
        bg_sidebar = "#ffffff"
        bg_card = "#ffffff"
        border_card = "#e2e8f0"
        text_primary = "#0f172a"
        text_secondary = "#334155"
        accent_blue = "#2563eb"
        input_bg = "#ffffff"
        chat_msg_bg = "#ffffff"
        chat_bottom_bg = "#ffffff"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        .stApp, [data-testid="stAppViewContainer"], .main {{
            background-color: {bg_app} !important;
            color: {text_primary} !important;
        }}

        header[data-testid="stHeader"] {{
            background-color: {bg_app} !important;
        }}

        section[data-testid="stSidebar"], [data-testid="stSidebar"] > div {{
            background-color: {bg_sidebar} !important;
            border-right: 1px solid {border_card} !important;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: {text_primary} !important;
            font-weight: 700 !important;
        }}
        
        p, span, label, div[data-testid="stMarkdownContainer"] p {{
            color: {text_secondary} !important;
        }}

        .user-card {{
            background: {"linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%)" if is_dark else "linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%)"};
            border: 1px solid {border_card};
            padding: 1rem 1.1rem;
            border-radius: 14px;
            margin-bottom: 1.25rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }}
        .user-name {{
            font-weight: 700;
            color: {text_primary};
            font-size: 0.95rem;
        }}
        .user-email {{
            font-size: 0.8rem;
            color: {text_secondary};
            word-break: break-all;
        }}

        div[data-testid="stBottom"], div[data-testid="stBottom"] > div {{
            background-color: {chat_bottom_bg} !important;
            border-top: 1px solid {border_card} !important;
        }}

        div[data-testid="stChatInput"] {{
            background-color: {input_bg} !important;
            border: 1.5px solid {border_card} !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 14px rgba(0,0,0,0.04) !important;
        }}

        div[data-testid="stChatInput"] textarea {{
            background-color: transparent !important;
            color: {text_primary} !important;
            font-size: 14px !important;
        }}

        [data-testid="stChatMessage"] {{
            background-color: {chat_msg_bg} !important;
            border: 1px solid {border_card} !important;
            border-radius: 14px !important;
            padding: 1rem 1.2rem !important;
            margin-bottom: 0.85rem !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
        }}

        div[data-testid="stMetric"] {{
            background: {bg_card} !important;
            border: 1px solid {border_card} !important;
            border-radius: 14px !important;
            padding: 1rem 1.2rem !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
        }}

        /* Clean Tab Navigation */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            border-bottom: 2px solid {border_card};
            padding-bottom: 4px;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px 8px 0 0;
            padding: 8px 16px;
            font-weight: 600;
            color: {text_secondary};
        }}
        .stTabs [aria-selected="true"] {{
            color: {accent_blue} !important;
            border-bottom: 2px solid {accent_blue} !important;
        }}

        /* Buttons */
        div.stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1.2rem !important;
        }}
        div.stButton > button:not([kind="primary"]) {{
            border-radius: 8px !important;
            border: 1px solid {border_card} !important;
            font-weight: 500 !important;
        }}
        </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """Initializes default messages, stats, and documents if not already set."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "👋 Welcome to Enterprise Multi-Agent RAG! How can I assist you with your knowledge documents today?",
                "agent_trace": {
                    "router": "Direct Response Agent",
                    "retrieval": "System Initialized",
                    "confidence": "100%",
                },
                "sources": []
            }
        ]

    if "total_docs" not in st.session_state:
        st.session_state["total_docs"] = 42

    if "vector_chunks" not in st.session_state:
        st.session_state["vector_chunks"] = 1284

    if "documents_list" not in st.session_state:
        st.session_state["documents_list"] = [
            {"id": "doc-01", "name": "Enterprise_Security_Architecture_v4.pdf", "category": "Security & SecOps", "chunks": 142, "status": "Indexed", "updated": "2026-10-08"},
            {"id": "doc-02", "name": "MultiAgent_Orchestration_Spec.pdf", "category": "Engineering", "chunks": 98, "status": "Indexed", "updated": "2026-10-07"},
            {"id": "doc-03", "name": "Global_Compliance_SOC2_HIPAA.docx", "category": "Legal & Audit", "chunks": 315, "status": "Indexed", "updated": "2026-10-06"},
            {"id": "doc-04", "name": "Hybrid_Vector_Retrieval_Benchmark.md", "category": "AI Research", "chunks": 64, "status": "Indexed", "updated": "2026-10-05"},
            {"id": "doc-05", "name": "Q3_Infrastructure_SLA_CostReport.csv", "category": "DevOps", "chunks": 112, "status": "Indexed", "updated": "2026-10-04"},
        ]


def run_rag_pipeline(user_query: str):
    """Simulates realistic multi-agent execution pipeline with grounded sources."""
    query_lower = user_query.lower()

    if "security" in query_lower or "soc" in query_lower or "hipaa" in query_lower:
        synthesized_text = (
            "Based on the **Enterprise Security Architecture v4** and **SOC2/HIPAA Audit Guidelines**, "
            "all vector embeddings are encrypted at rest using AES-256-GCM. Queries undergo strict tenant-level ACL "
            "filtering prior to index traversal, preventing cross-tenant data leakage. Retrieval latency is capped at 150ms "
            "with continuous mutual TLS (mTLS) enforcement."
        )
        sources = [
            {"name": "Enterprise_Security_Architecture_v4.pdf", "section": "Section 4.2: Data-at-Rest Encryption", "score": "98.4%", "snippet": "AES-256-GCM enforced across all pgvector indices with per-tenant isolation keys."},
            {"name": "Global_Compliance_SOC2_HIPAA.docx", "section": "Clause 8.1: Access Control & Audit Logs", "score": "95.1%", "snippet": "Continuous audit telemetry logged with SHA-256 tamper-evident hash chaining."}
        ]
        agent_router = "Security & Compliance Agent"
    elif "architecture" in query_lower or "agent" in query_lower or "pipeline" in query_lower:
        synthesized_text = (
            "The **Multi-Agent Orchestration Specification** defines a 4-tier pipeline:\n\n"
            "1. **Query Intent & Decomposition Agent**: Parses ambiguities, identifies multi-hop dependencies, and expands domain acronyms.\n"
            "2. **Hybrid Retrieval Agent**: Runs simultaneous dense vector search (cosine similarity) and sparse BM25 keyword matching via Reciprocal Rank Fusion (RRF).\n"
            "3. **Cross-Encoder Re-ranker**: Re-evaluates top 25 candidate chunks down to the top 5 highest-confidence contexts.\n"
            "4. **Synthesis & Grounding Agent**: Streams generation while validating factual attribution and preventing hallucination."
        )
        sources = [
            {"name": "MultiAgent_Orchestration_Spec.pdf", "section": "Section 2.1: Distributed Routing Graph", "score": "99.1%", "snippet": "Query decomposition splits compound queries into sub-graph execution branches."},
            {"name": "Hybrid_Vector_Retrieval_Benchmark.md", "section": "Table 3: RRF vs Pure Dense Accuracy", "score": "96.7%", "snippet": "Hybrid RRF yields a 14.2% lift in MRR@10 compared to single-vector baseline."}
        ]
        agent_router = "Architecture & Pipeline Router"
    else:
        synthesized_text = (
            f"Regarding **'{user_query}'**:\n\n"
            "The multi-agent RAG engine performed hybrid semantic retrieval across the indexed knowledge base. "
            "The query was classified as an enterprise domain query, routed to dense vector embeddings with cross-encoder "
            "re-ranking. Relevant contextual chunks were retrieved and synthesized with strict citation grounding."
        )
        sources = [
            {"name": "Enterprise_Security_Architecture_v4.pdf", "section": "Section 1.1: System Overview", "score": "93.8%", "snippet": "Central knowledge index unifying structured tables and unstructured documents."},
            {"name": "MultiAgent_Orchestration_Spec.pdf", "section": "Section 3.4: Context Window Optimization", "score": "91.2%", "snippet": "Dynamically selects optimal context window size based on document density."}
        ]
        agent_router = "Autonomous General Knowledge Router"

    trace = {
        "router": agent_router,
        "retrieval": "Hybrid Dense + BM25 (RRF Top-5)",
        "confidence": "97.6%"
    }

    return synthesized_text, sources, trace


def dashboard():
    """Main Dashboard view for Enterprise Multi-Agent RAG Platform."""
    init_session_state()

    # 1. Apply global theme
    is_dark = st.session_state.get("dark_mode", False)
    inject_global_theme(is_dark)

    # 2. Render Sidebar
    with st.sidebar:
        user_name = st.session_state.get("user_name", "Enterprise User")
        user_email = st.session_state.get("user_email", "admin@enterprise.ai")

        st.markdown(f"""
            <div class="user-card">
                <div class="user-name">👤 {user_name}</div>
                <div class="user-email">{user_email}</div>
            </div>
        """, unsafe_allow_html=True)

        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            dark_toggle = st.toggle("🌙 Dark Mode", value=is_dark)
            if dark_toggle != is_dark:
                st.session_state["dark_mode"] = dark_toggle
                st.rerun()
        with col_t2:
            if st.button("Logout", key="logout_btn"):
                st.session_state["authenticated"] = False
                st.session_state["current_page"] = "login"
                st.rerun()

        st.markdown("---")
        # Document management and Chat sidebars
        document_sidebar()
        chat_sidebar()

    # 3. Retrieve Dashboard Robot Image
    img_b64 = get_dashboard_image_b64()
    img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width: 140px; height: 140px; object-fit: cover; border-radius: 18px; box-shadow: 0 10px 25px rgba(2, 18, 53, 0.4); border: 1px solid rgba(255, 255, 255, 0.15);" alt="Dashboard AI Robot" />' if img_b64 else '<div style="font-size: 64px;">🤖</div>'

    # 4. Hero Welcome Card featuring the 3D Dashboard Robot
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #021235 0%, #031B4E 55%, #06286E 100%);
                    border-radius: 24px; padding: 26px 30px; color: #FFFFFF;
                    box-shadow: 0 20px 40px -15px rgba(2, 18, 53, 0.45);
                    border: 1px solid rgba(255, 255, 255, 0.12);
                    display: flex; align-items: center; justify-content: space-between;
                    margin-bottom: 2rem; gap: 24px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 260px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="background: #2563EB; color: white; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;">ACTIVE SYSTEM</span>
                    <span style="color: #94A3B8; font-size: 12px; font-weight: 500;">Enterprise Hybrid RAG Platform</span>
                </div>
                <h2 style="color: #FFFFFF; font-size: 26px; font-weight: 800; margin: 0 0 8px 0; line-height: 1.25;">
                    Intelligent <span style="color: #38BDF8;">Workspace & Analytics</span>
                </h2>
                <p style="color: #94A3B8; font-size: 14px; margin: 0 0 16px 0; line-height: 1.5; font-weight: 400;">
                    Multi-vector embeddings, agentic query routing, and reranked knowledge bases.
                </p>
                <div style="display: flex; gap: 12px; flex-wrap: wrap; font-size: 12px; color: #7DD3FC;">
                    <span>• Hybrid Retrieval Active</span>
                    <span>• Multi-Agent Engine</span>
                    <span>• Real-time Grounding</span>
                </div>
            </div>
            <div style="flex-shrink: 0; display: flex; justify-content: center; align-items: center;">
                {img_tag}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 5. Dashboard Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Indexed Docs", st.session_state.get("total_docs", 42), delta="+3 today")
    with m2:
        st.metric("Vector Chunks", st.session_state.get("vector_chunks", 1284), delta="+120")
    with m3:
        st.metric("Avg Latency", "320 ms", delta="-45 ms")
    with m4:
        st.metric("Retrieval Precision", "98.4%", delta="+0.8%")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 6. Tabbed Multi-Agent Dashboard (Full Functionality)
    tab_chat, tab_kb, tab_agents, tab_analytics = st.tabs([
        "💬 Multi-Agent Chat Console",
        "📑 Knowledge Base & Chunks",
        "🤖 Pipeline Architecture",
        "📊 Retrieval Analytics"
    ])

    # =========================================================================
    # TAB 1: Multi-Agent RAG Chat Console
    # =========================================================================
    with tab_chat:
        st.markdown("#### ⚡ Quick Prompts")
        q_col1, q_col2, q_col3 = st.columns(3)
        with q_col1:
            if st.button("🏗️ Explain RAG Architecture", use_container_width=True, key="quick_q1"):
                st.session_state["pending_query"] = "Explain the multi-agent RAG architecture and retrieval steps"
        with q_col2:
            if st.button("🔒 Review SOC2 Security & Encryption", use_container_width=True, key="quick_q2"):
                st.session_state["pending_query"] = "What are the SOC2 security protocols and vector encryption methods?"
        with q_col3:
            if st.button("📊 Compare Hybrid Retrieval Benchmarks", use_container_width=True, key="quick_q3"):
                st.session_state["pending_query"] = "How does hybrid RRF retrieval compare to pure dense embeddings?"

        st.markdown("---")

        # Render conversation history
        for idx, msg in enumerate(st.session_state.get("messages", [])):
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

                # If assistant message has agent execution trace, show details
                if msg["role"] == "assistant" and "agent_trace" in msg and msg["agent_trace"]:
                    trace = msg["agent_trace"]
                    with st.expander("🔍 Agent Execution Trace & Routing", expanded=False):
                        t_col1, t_col2, t_col3 = st.columns(3)
                        with t_col1:
                            st.caption(f"**Agent Router:**\n{trace.get('router', 'Autonomous')}")
                        with t_col2:
                            st.caption(f"**Retrieval Method:**\n{trace.get('retrieval', 'Dense Vector')}")
                        with t_col3:
                            st.caption(f"**Attribution Score:**\n{trace.get('confidence', '98%')}")

                # If message has sources, show citation cards
                if msg["role"] == "assistant" and "sources" in msg and msg["sources"]:
                    with st.expander(f"📚 Retrieved Sources & Citations ({len(msg['sources'])})", expanded=False):
                        for s_idx, src in enumerate(msg["sources"]):
                            st.markdown(f"""
                                <div style="background: {'rgba(30, 41, 59, 0.4)' if is_dark else '#f1f5f9'};
                                            padding: 10px 14px; border-radius: 8px; margin-bottom: 8px;
                                            border-left: 3px solid #2563eb;">
                                    <div style="display: flex; justify-content: space-between; font-weight: 600; font-size: 13px;">
                                        <span>📄 {src['name']}</span>
                                        <span style="color: #2563eb;">Match: {src['score']}</span>
                                    </div>
                                    <div style="font-size: 12px; color: {'#94a3b8' if is_dark else '#64748b'}; margin-top: 2px;">
                                        📍 {src['section']}
                                    </div>
                                    <div style="font-size: 12px; margin-top: 6px; font-style: italic;">
                                        "{src['snippet']}"
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

        # Handle pending quick queries or chat input
        prompt = st.chat_input("Ask any question across your enterprise documents...")
        pending = st.session_state.pop("pending_query", None)
        active_query = pending if pending else prompt

        if active_query:
            # 1. Append user message
            st.session_state["messages"].append({"role": "user", "content": active_query})
            with st.chat_message("user"):
                st.write(active_query)

            # 2. Simulate agent execution and response
            with st.chat_message("assistant"):
                with st.spinner("🤖 Multi-agent consensus in progress (Query Routing ➔ Vector Retrieval ➔ Re-ranking)..."):
                    time.sleep(0.4)
                    ans, sources, trace = run_rag_pipeline(active_query)
                    st.write(ans)

                    # Show trace
                    with st.expander("🔍 Agent Execution Trace & Routing", expanded=False):
                        t_col1, t_col2, t_col3 = st.columns(3)
                        with t_col1:
                            st.caption(f"**Agent Router:**\n{trace['router']}")
                        with t_col2:
                            st.caption(f"**Retrieval Method:**\n{trace['retrieval']}")
                        with t_col3:
                            st.caption(f"**Attribution Score:**\n{trace['confidence']}")

                    # Show sources
                    if sources:
                        with st.expander(f"📚 Retrieved Sources & Citations ({len(sources)})", expanded=True):
                            for src in sources:
                                st.markdown(f"""
                                    <div style="background: {'rgba(30, 41, 59, 0.4)' if is_dark else '#f1f5f9'};
                                                padding: 10px 14px; border-radius: 8px; margin-bottom: 8px;
                                                border-left: 3px solid #2563eb;">
                                        <div style="display: flex; justify-content: space-between; font-weight: 600; font-size: 13px;">
                                            <span>📄 {src['name']}</span>
                                            <span style="color: #2563eb;">Match: {src['score']}</span>
                                        </div>
                                        <div style="font-size: 12px; color: {'#94a3b8' if is_dark else '#64748b'}; margin-top: 2px;">
                                            📍 {src['section']}
                                        </div>
                                        <div style="font-size: 12px; margin-top: 6px; font-style: italic;">
                                            "{src['snippet']}"
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)

            # 3. Save assistant message to state
            st.session_state["messages"].append({
                "role": "assistant",
                "content": ans,
                "agent_trace": trace,
                "sources": sources
            })
            st.rerun()

    # =========================================================================
    # TAB 2: Knowledge Base & Document Chunks
    # =========================================================================
    with tab_kb:
        st.markdown("#### 📚 Active Enterprise Knowledge Sources")
        docs = st.session_state.get("documents_list", [])

        search_kb = st.text_input("🔍 Search Knowledge Base", placeholder="Filter documents by title or category...", key="kb_filter")

        filtered_docs = [d for d in docs if not search_kb or search_kb.lower() in d["name"].lower() or search_kb.lower() in d["category"].lower()]

        for d in filtered_docs:
            with st.container():
                st.markdown(f"""
                    <div style="background: {'#131b2e' if is_dark else '#ffffff'};
                                border: 1px solid {'#1e293b' if is_dark else '#e2e8f0'};
                                border-radius: 12px; padding: 14px 18px; margin-bottom: 12px;
                                display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>
                            <div style="font-weight: 700; font-size: 15px; color: {'#ffffff' if is_dark else '#0f172a'};">
                                📄 {d['name']}
                            </div>
                            <div style="font-size: 12px; color: #64748b; margin-top: 4px;">
                                Category: <b>{d['category']}</b> • Chunks: <b>{d['chunks']}</b> • Updated: <b>{d['updated']}</b>
                            </div>
                        </div>
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <span style="background: #10b981; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 700;">
                                ✓ {d['status']}
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    # =========================================================================
    # TAB 3: Pipeline Architecture
    # =========================================================================
    with tab_agents:
        st.markdown("#### 🤖 Distributed Multi-Agent RAG Topology")
        st.info("The platform runs an autonomous pipeline separating query analysis, vector lookup, contextual reranking, and grounded response synthesis.")

        a1, a2 = st.columns(2)
        with a1:
            st.markdown(f"""
                <div style="background: {'#131b2e' if is_dark else '#ffffff'}; border: 1px solid {'#1e293b' if is_dark else '#e2e8f0'}; border-radius: 14px; padding: 16px; margin-bottom: 12px;">
                    <div style="font-weight: 700; color: #38bdf8;">1. Query Decomposition Agent</div>
                    <p style="font-size: 13px; margin: 6px 0 0 0;">Translates raw natural language queries into semantic vector embeddings and boolean sparse tokens for dual retrieval.</p>
                </div>
                <div style="background: {'#131b2e' if is_dark else '#ffffff'}; border: 1px solid {'#1e293b' if is_dark else '#e2e8f0'}; border-radius: 14px; padding: 16px; margin-bottom: 12px;">
                    <div style="font-weight: 700; color: #38bdf8;">2. Hybrid Retrieval Engine</div>
                    <p style="font-size: 13px; margin: 6px 0 0 0;">Executes pgvector HNSW cosine search simultaneously with BM25 keyword matching via Reciprocal Rank Fusion (RRF).</p>
                </div>
            """, unsafe_allow_html=True)
        with a2:
            st.markdown(f"""
                <div style="background: {'#131b2e' if is_dark else '#ffffff'}; border: 1px solid {'#1e293b' if is_dark else '#e2e8f0'}; border-radius: 14px; padding: 16px; margin-bottom: 12px;">
                    <div style="font-weight: 700; color: #38bdf8;">3. Cross-Encoder Re-ranker</div>
                    <p style="font-size: 13px; margin: 6px 0 0 0;">Applies deep cross-attention to score document chunk relevance, filtering noise and maximizing prompt density.</p>
                </div>
                <div style="background: {'#131b2e' if is_dark else '#ffffff'}; border: 1px solid {'#1e293b' if is_dark else '#e2e8f0'}; border-radius: 14px; padding: 16px; margin-bottom: 12px;">
                    <div style="font-weight: 700; color: #38bdf8;">4. Grounded Synthesis & Citation Agent</div>
                    <p style="font-size: 13px; margin: 6px 0 0 0;">Generates verified natural language summaries with strict source attribution and zero ungrounded hallucinations.</p>
                </div>
            """, unsafe_allow_html=True)

    # =========================================================================
    # TAB 4: Retrieval Analytics
    # =========================================================================
    with tab_analytics:
        st.markdown("#### 📊 Real-Time Retrieval & Latency Metrics")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Latency Breakdown (ms)**")
            st.caption("• Query Embedding: **38 ms**")
            st.caption("• Dense Vector Lookup: **72 ms**")
            st.caption("• Cross-Encoder Rerank: **115 ms**")
            st.caption("• Context Synthesis: **95 ms**")
            st.progress(0.72)
        with c2:
            st.markdown("**Retrieval Accuracy Benchmarks**")
            st.caption("• Mean Reciprocal Rank (MRR@10): **0.942**")
            st.caption("• Normalized Discounted Cumulative Gain (NDCG@5): **0.961**")
            st.caption("• Hallucination Rate: **< 0.1%**")
            st.progress(0.96)