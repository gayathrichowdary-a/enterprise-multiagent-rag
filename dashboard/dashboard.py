# dashboard/dashboard.py
import streamlit as st
from dashboard.upload import document_sidebar
from dashboard.chat import chat_sidebar

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
        text_primary = "#0f172a"
        text_secondary = "#64748b"
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
    """Main dashboard layout and navigation sidebar."""
    user = st.session_state.get("user", {})
    user_name = user.get("full_name") or user.get("name", "Gayathri")
    user_email = user.get("email", "enterprise@system.ai")

    with st.sidebar:
        # Platform Logo
        st.markdown("""
            <div style="margin-bottom: 1rem;">
                <div style="display: inline-block; background: #2563eb; color: white; padding: 3px 8px; border-radius: 6px; font-weight: 800; font-size: 0.72rem; margin-bottom: 6px;">ENTERPRISE</div>
                <h2 style="font-size: 1.18rem; font-weight: 800; margin: 0; line-height: 1.2;">🤖 Adaptive Multi-Agent RAG</h2>
            </div>
        """, unsafe_allow_html=True)

        # User Card
        st.markdown(f"""
            <div class="user-card">
                <div class="user-name">🟢 {user_name}</div>
                <div class="user-email">{user_email}</div>
            </div>
        """, unsafe_allow_html=True)

        # Theme Toggle (without any dangerous st.rerun loop)
        st.caption("THEME DISPLAY")
        is_dark_mode = st.toggle("🌙 Dark Cyber Mode", value=st.session_state.get("ui_is_dark", False), key="ui_is_dark")

        st.caption("NAVIGATION MENU")
        page = st.radio(
            "Navigation Menu",
            [
                "🏠 Home",
                "📤 Upload Documents",
                "💬 Chat",
                "⚖️ Compare Documents",
                "🕸️ Knowledge Graph",
                "📊 Source Rankings",
                "🧠 Memory",
                "📜 History",
                "⚙️ Settings",
                "🚪 Logout"
            ],
            label_visibility="collapsed"
        )

        st.divider()

        if page == "📤 Upload Documents":
            document_sidebar()
        elif page == "💬 Chat":
            chat_sidebar()

        st.caption("🛡️ Adaptive Engine v2.4 Active")

    # Inject theme based on toggle state
    inject_global_theme(is_dark_mode)

    return page