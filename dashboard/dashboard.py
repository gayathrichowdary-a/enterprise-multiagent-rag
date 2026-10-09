import os
import base64
import streamlit as st
from dashboard.upload import document_sidebar
from dashboard.chat import chat_sidebar

def get_dashboard_image_b64():
    """Retrieve base64 image string for dashboard robot, checking assets and local folders."""
    possible_paths = [
        "assets/dashboard_robot.png",
        "assets/dashboard_robot.jpg",
        "assets/dashboard_robot.jpeg",
        "dashboard/dashboard_robot.png",
        "dashboard/dashboard_robot.jpg",
        "dashboard_robot.png",
        "dashboard_robot.jpg",
        "assets/image.png",
        "assets/login_robot.jpg"
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
    """Applies clean Light or Full Cyber Dark mode across EVERY page."""
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
        text_primary = "#000000"
        text_secondary = "#0f172a"
        accent_blue = "#2563eb"
        input_bg = "#ffffff"
        chat_msg_bg = "#ffffff"
        chat_bottom_bg = "#ffffff"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

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
        }}
        p, span, label, div[data-testid="stMarkdownContainer"] p {{
            color: {text_secondary} !important;
        }}

        .user-card {{
            background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%) if {is_dark} else linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
            border: 1px solid {border_card};
            padding: 0.9rem 1rem;
            border-radius: 12px;
            margin-bottom: 1.25rem;
        }}
        .user-name {{
            font-weight: 700;
            color: {text_primary};
            font-size: 0.95rem;
        }}
        .user-email {{
            font-size: 0.78rem;
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
        }}

        div[data-testid="stChatInput"] textarea {{
            background-color: transparent !important;
            color: {text_primary} !important;
        }}

        [data-testid="stChatMessage"] {{
            background-color: {chat_msg_bg} !important;
            border: 1px solid {border_card} !important;
            border-radius: 12px !important;
        }}

        div[data-testid="stMetric"] {{
            background: {bg_card} !important;
            border: 1px solid {border_card} !important;
            border-radius: 12px !important;
        }}

        div.stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: #ffffff !important;
            border: none !important;
        }}
        </style>
    """, unsafe_allow_html=True)


def dashboard():
    st.markdown('''
        <style>
        /* Force crisp black text across all cards, paragraphs, and markdown in Light Mode */
        html, body, [data-testid="stAppViewContainer"] {
            color: #0f172a !important;
        }
        p, span, label, div {
            color: #0f172a !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #000000 !important;
            font-weight: 700 !important;
        }
        [data-testid="stVerticalBlock"] p {
            color: #1e293b !important;
        }
        </style>
    ''', unsafe_allow_html=True)

    # 1. Apply global theme
    is_dark = st.session_state.get("dark_mode", False)
    inject_global_theme(is_dark)

    # 2. Render Sidebar with user info and sidebar handlers
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
        # Keep both of your sidebar functions
        document_sidebar()
        chat_sidebar()

    # 3. Retrieve Dashboard Robot Image
    img_b64 = get_dashboard_image_b64()
    img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width: 140px; height: 140px; object-fit: cover; border-radius: 18px; box-shadow: 0 10px 25px rgba(2, 18, 53, 0.4); border: 1px solid rgba(255, 255, 255, 0.15);" alt="Dashboard AI Robot" />' if img_b64 else '<div style="font-size: 64px;">🤖</div>'

    # 4. Hero Welcome Card featuring the Dashboard Robot
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