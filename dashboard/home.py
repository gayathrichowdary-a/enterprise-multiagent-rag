# dashboard/home.py
import streamlit as st

def home_page():
    # ---------------------------------------------------------
    # 1. LANGUAGE & THEME CONTROLS (TOP HEADER)
    # ---------------------------------------------------------
    if "app_language" not in st.session_state:
        st.session_state.app_language = "English"

    is_dark = st.session_state.get("ui_theme", "Light") == "Dark"

    # Top Row: Title on Left, Language Switcher on Top-Right
    col_title, col_lang = st.columns([3.8, 1.4])
    
    with col_lang:
        lang_choice = st.segmented_control(
            "Language / భాష",
            ["🌐 English", "🇮🇳 తెలుగు"],
            default="🇮🇳 తెలుగు" if st.session_state.app_language == "Telugu" else "🌐 English",
            label_visibility="collapsed"
        )
        st.session_state.app_language = "Telugu" if "తెలుగు" in (lang_choice or "") else "English"

    is_telugu = st.session_state.app_language == "Telugu"

    # Multilingual Content Dictionary
    content = {
        "title": "రక్షిత మల్టీ-ఏజెంట్ ఎంటర్‌ప్రైజ్ RAG" if is_telugu else "🛡️ Adaptive Multi-Agent Enterprise RAG",
        "subtitle": "గ్రాఫ్ RAG మరియు ARES క్వాలిటీ వెరిఫికేషన్‌తో ఆధునిక నాలెడ్జ్ ఇంటెలిజెన్స్" if is_telugu else "Next-Generation Knowledge Intelligence with Graph RAG & ARES Quality Verification",
        "welcome": "తిరిగి స్వాగతం" if is_telugu else "Welcome back",
        "welcome_desc": "మీ అడాప్టివ్ నాలెడ్జ్ నెట్‌వర్క్ క్రియాశీలంగా ఉంది. పత్రాల విశ్లేషణ, నాలెడ్జ్ గ్రాఫ్స్ మరియు నిర్ధారిత సమాధానాల కోసం సిద్ధంగా ఉంది." if is_telugu else "Your adaptive multi-agent knowledge mesh is fully operational. Ready to ingest documents, traverse knowledge subgraphs, and verify grounded reasoning.",
        "stat_docs": "క్రియాశీల పత్రాలు" if is_telugu else "Active Documents",
        "stat_pipeline": "లాంగ్‌గ్రాఫ్ పైప్‌లైన్" if is_telugu else "LangGraph Pipeline",
        "stat_trust": "విశ్వసనీయత రేటింగ్" if is_telugu else "Avg Source Trust",
        "stat_ares": "ARES విశ్వసనీయ పరిమితి" if is_telugu else "ARES PPI Bounds",
        "arch_title": "మల్టీ-ఏజెంట్ ఆర్కిటెక్చర్ పైప్‌లైన్ (LangGraph)" if is_telugu else "Multi-Agent Orchestration Architecture (LangGraph)",
        "arch_desc": "ప్రశ్న నుంచి హైబ్రిడ్ రిట్రీవల్ మరియు ARES నిర్ధారణ వరకు కొనసాగే ప్రక్రియ ప్రవాహం." if is_telugu else "Live execution pipeline: State transitions from query intent to hybrid grounding and ARES verification.",
        "pillars_title": "ముఖ్యమైన సాంకేతిక విభాగాలు" if is_telugu else "Core Architectural Pillars",
        "p1_title": "హైబ్రిడ్ రిట్రీవల్ & అథారిటీ ర్యాంకింగ్" if is_telugu else "Adaptive Hybrid Retrieval",
        "p1_desc": "వెక్టర్ సెర్చ్ (FAISS) మరియు నాలెడ్జ్ గ్రాఫ్‌లను కలిపి ఉన్నతమైన పాలసీ డాక్యుమెంట్లకు అధిక ప్రాధాన్యతనిస్తుంది." if is_telugu else "Combines dense semantic vector search (FAISS) with structured entity relations (Graph RAG). Dynamic source reliability multipliers prioritize official Tier 1 policies over informal working notes.",
        "p2_title": "ARES క్వాలిటీ మూల్యాంకనం" if is_telugu else "ARES Quality Evaluation",
        "p2_desc": "స్టాన్‌ఫోర్డ్ ARES విధానంతో సందర్భం, నిజాయితీ (Faithfulness) మరియు విశ్వసనీయతను 95% నిర్ధారణతో లెక్కిస్తుంది." if is_telugu else "Implements Stanford's ARES benchmark with Prediction-Powered Inference (PPI). Automatically validates context relevance, grounded faithfulness, and answer alignment with 95% confidence intervals.",
        "p3_title": "ద్విముఖ మెమరీ సిస్టమ్" if is_telugu else "Dual-Tier Memory System",
        "p3_desc": "తాజా చాట్ సంభాషణలను (ఎపిసోడిక్) మరియు యూజర్ ప్రొఫైల్ ప్రాధాన్యతలను నిరంతరం నిక్షిప్తం చేస్తుంది." if is_telugu else "Episodic conversation memory retains session context while persistent profile memory stores role-based user preferences, departments, and compliance rules across restarts.",
        "p4_title": "పత్రాల పోలిక & వివాద పరిష్కారం" if is_telugu else "Multi-Doc Comparison & Conflict Resolution",
        "p4_desc": "వివిధ పత్రాలను సమాంతరంగా విశ్లేషించి తేడాలను గుర్తించి, అథారిటీ నిబంధనల ఆధారంగా ఖచ్చితమైన నిర్ణయాన్ని ఇస్తుంది." if is_telugu else "Cross-analyzes multiple uploaded documents side-by-side. Highlights discrepancies, extracts overlapping clauses, and resolves ambiguities using authority tier precedence rules."
    }

    with col_title:
        st.markdown(f"<h1 style='margin-bottom:0;'>{content['title']}</h1>", unsafe_allow_html=True)
        st.caption(content['subtitle'])

    # Dynamic Palette
    if is_dark:
        bg_card = "#131b2e"
        border_card = "#1e293b"
        text_primary = "#ffffff"
        text_secondary = "#94a3b8"
        hero_bg = "linear-gradient(135deg, #111827 0%, #1e1b4b 100%)"
        accent_blue = "#38bdf8"
        graph_bg = "#090d16"
        node_fill = "#1e293b"
        node_font = "#ffffff"
    else:
        bg_card = "#ffffff"
        border_card = "#e2e8f0"
        text_primary = "#0f172a"
        text_secondary = "#64748b"
        hero_bg = "linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%)"
        accent_blue = "#2563eb"
        graph_bg = "#ffffff"
        node_fill = "#ffffff"
        node_font = "#1e293b"

    st.markdown(f"""
        <style>
        .hero-banner {{
            background: {hero_bg};
            padding: 2rem 2.2rem;
            border-radius: 16px;
            border: 1px solid {border_card};
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.25);
        }}
        .hero-banner h3 {{
            color: #ffffff !important;
            font-size: 1.55rem !important;
            font-weight: 800 !important;
        }}
        .hero-banner p {{
            color: #cbd5e1 !important;
            font-size: 0.96rem !important;
        }}
        .stat-card {{
            background-color: {bg_card};
            border: 1px solid {border_card};
            padding: 1.25rem 1rem;
            border-radius: 14px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: transform 0.2s ease;
        }}
        .stat-card:hover {{
            transform: translateY(-3px);
            border-color: {accent_blue};
        }}
        .stat-val {{
            font-size: 1.8rem;
            font-weight: 800;
            color: {accent_blue};
        }}
        .stat-lbl {{
            font-size: 0.76rem;
            font-weight: 700;
            color: {text_secondary};
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-top: 4px;
        }}
        .feature-card {{
            background-color: {bg_card};
            border: 1px solid {border_card};
            padding: 1.35rem;
            border-radius: 14px;
            height: 100%;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        }}
        .feature-card h4 {{
            color: {text_primary} !important;
            font-weight: 700 !important;
        }}
        .feature-card p {{
            color: {text_secondary} !important;
            line-height: 1.5;
        }}
        </style>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 2. HERO GREETING BANNER
    # ---------------------------------------------------------
    user = st.session_state.get("user", {})
    user_name = user.get("full_name") or user.get("name", "Gayathri")

    st.markdown(f"""
        <div class="hero-banner">
            <h3 style="margin:0;">{content['welcome']}, {user_name}! 👋</h3>
            <p style="margin: 0.5rem 0 0 0;">
                {content['welcome_desc']}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 3. LIVE PLATFORM TELEMETRY CARDS (GRID LAYOUT)
    # ---------------------------------------------------------
    docs_count = len(st.session_state.get("vector_stores", {}))
    sources_data = st.session_state.get("knowledge_sources", {})
    avg_trust = (sum([v.get("reliability_score", 80) for v in sources_data.values()]) / max(1, len(sources_data))) if sources_data else 95.0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val">{docs_count}</div>
                <div class="stat-lbl">{content['stat_docs']}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val">8 Nodes</div>
                <div class="stat-lbl">{content['stat_pipeline']}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val">{avg_trust:.1f}%</div>
                <div class="stat-lbl">{content['stat_trust']}</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val">95% CI</div>
                <div class="stat-lbl">{content['stat_ares']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ---------------------------------------------------------
    # 4. INTERACTIVE MULTI-AGENT ORCHESTRATION FLOW (GRAPH)
    # ---------------------------------------------------------
    st.subheader(f"🔄 {content['arch_title']}")
    st.caption(content['arch_desc'])

    # Node labels translated if Telugu selected
    q_lbl = "👤 యూజర్ ప్రశ్న" if is_telugu else "👤 User Query"
    r_lbl = "🤖 రూటర్ ఏజెంట్" if is_telugu else "🤖 Router Agent"
    v_lbl = "📚 వెక్టర్ స్టోర్ (FAISS)" if is_telugu else "📚 Vector Store (FAISS)"
    g_lbl = "🕸️ నాలెడ్జ్ గ్రాఫ్" if is_telugu else "🕸️ Knowledge Graph Subgraph"
    w_lbl = "🌐 వెబ్ సెర్చ్ (Tavily)" if is_telugu else "🌐 Tavily Fallback Search"
    h_lbl = "⚖️ అడాప్టివ్ రీ-ర్యాంకర్" if is_telugu else "⚖️ Adaptive Re-Ranker\\n(Tier 1/2/3 Multipliers)"
    m_lbl = "🧠 ప్రొఫైల్ & ఎపిసోడిక్ మెమరీ" if is_telugu else "🧠 Episodic & Profile Memory"
    a_lbl = "🛡️ ARES నాణ్యత తనిఖీ" if is_telugu else "🛡️ ARES Quality Triad\\n(Context, Faithfulness, Relevance)"
    ans_lbl = "🎯 ఖచ్చితమైన సమాధానం" if is_telugu else "🎯 Verified Final Answer\\n+ Exact Citations"

    dot_flow = f"""
    digraph LangGraphFlow {{
        rankdir=LR;
        bgcolor="{graph_bg}";
        
        node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=10, penwidth=1.5];
        edge [fontname="Helvetica", fontsize=9, color="#64748b", fontcolor="#94a3b8"];

        q [label="{q_lbl}", fillcolor="#312e81", fontcolor="#e0e7ff", color="#6366f1"];
        router [label="{r_lbl}", fillcolor="#78350f", fontcolor="#fef3c7", color="#f59e0b"];
        
        vec [label="{v_lbl}", fillcolor="{node_fill}", fontcolor="{node_font}", color="#475569"];
        graph [label="{g_lbl}", fillcolor="{node_fill}", fontcolor="{node_font}", color="#475569"];
        web [label="{w_lbl}", fillcolor="{node_fill}", fontcolor="{node_font}", color="#475569"];
        
        hybrid [label="{h_lbl}", fillcolor="#1e3a8a", fontcolor="#dbeafe", color="#3b82f6"];
        mem [label="{m_lbl}", fillcolor="#134e4a", fontcolor="#ccfbf1", color="#14b8a6"];
        
        ares [label="{a_lbl}", fillcolor="#7f1d1d", fontcolor="#fee2e2", color="#ef4444"];
        ans [label="{ans_lbl}", fillcolor="#14532d", fontcolor="#dcfce7", color="#22c55e"];

        q -> router;
        router -> vec;
        router -> graph;
        router -> web;
        
        vec -> hybrid;
        graph -> hybrid;
        hybrid -> ares;
        mem -> ares;
        ares -> ans;
    }}
    """
    st.graphviz_chart(dot_flow, use_container_width=True)

    st.write("")

    # ---------------------------------------------------------
    # 5. CORE SYSTEM CAPABILITIES GRID (MODERN 4-CARD TILES)
    # ---------------------------------------------------------
    st.subheader(f"⚡ {content['pillars_title']}")
    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown(f"""
            <div class="feature-card">
                <h4 style="margin:0 0 8px 0;">🔍 {content['p1_title']}</h4>
                <p style="font-size: 0.88rem; margin:0;">
                    {content['p1_desc']}
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown(f"""
            <div class="feature-card">
                <h4 style="margin:0 0 8px 0;">🛡️ {content['p2_title']}</h4>
                <p style="font-size: 0.88rem; margin:0;">
                    {content['p2_desc']}
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col_p2:
        st.markdown(f"""
            <div class="feature-card">
                <h4 style="margin:0 0 8px 0;">🧠 {content['p3_title']}</h4>
                <p style="font-size: 0.88rem; margin:0;">
                    {content['p3_desc']}
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown(f"""
            <div class="feature-card">
                <h4 style="margin:0 0 8px 0;">⚖️ {content['p4_title']}</h4>
                <p style="font-size: 0.88rem; margin:0;">
                    {content['p4_desc']}
                </p>
            </div>
        """, unsafe_allow_html=True)