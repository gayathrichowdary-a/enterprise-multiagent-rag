import streamlit as st
from dashboard.chat import chat_sidebar
from dashboard.user_info import get_current_user


# ---------------------------------------------------------------------------
# THEME
# ---------------------------------------------------------------------------
LIGHT = {
    "bg": "#ffffff",
    "sidebar_bg": "#f0f2f6",
    "card": "#ffffff",
    "card_grad": "linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%)",
    "border": "#bfdbfe",
    "text": "#1e293b",
    "muted": "#64748b",
    "accent": "#1e3a8a",
    "accent_soft": "#3b82f6",
    "input_bg": "#ffffff",
    "btn_bg": "#ffffff",
}

DARK = {
    "bg": "#0e1117",
    "sidebar_bg": "#161b22",
    "card": "#1c2128",
    "card_grad": "linear-gradient(135deg, #1e2a44 0%, #1c2128 100%)",
    "border": "#30363d",
    "text": "#e6edf3",
    "muted": "#9ba7b4",
    "accent": "#93c5fd",
    "accent_soft": "#60a5fa",
    "input_bg": "#21262d",
    "btn_bg": "#21262d",
}


def apply_theme():
    """Inject theme CSS. Call this on EVERY run (before any early return).

    It defines CSS variables on :root so any page can use them in custom HTML:
        background: var(--card); color: var(--text); border: 1px solid var(--border);
    """
    is_dark = st.session_state.get("dark_mode", False)
    t = DARK if is_dark else LIGHT

    css = f"""
    <style>
    :root {{
        --bg: {t['bg']};
        --sidebar-bg: {t['sidebar_bg']};
        --card: {t['card']};
        --card-grad: {t['card_grad']};
        --border: {t['border']};
        --text: {t['text']};
        --muted: {t['muted']};
        --accent: {t['accent']};
        --accent-soft: {t['accent_soft']};
        --input-bg: {t['input_bg']};
        --btn-bg: {t['btn_bg']};
    }}
    """

    # Only override Streamlit's own widgets in dark mode.
    # (Light mode uses Streamlit's defaults plus the variables above.)
    if is_dark:
        css += """
        /* App shell */
        .stApp,
        [data-testid="stApp"],
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background-color: var(--bg) !important;
            color: var(--text) !important;
        }
        [data-testid="stHeader"] {
            background-color: var(--bg) !important;
        }
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] > div {
            background-color: var(--sidebar-bg) !important;
        }

        /* Text */
        h1, h2, h3, h4, h5, h6,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] label,
        label, .stMarkdown {
            color: var(--text) !important;
        }
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p {
            color: var(--muted) !important;
        }
        hr { border-color: var(--border) !important; }

        /* Inputs */
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        [data-testid="stChatInput"] textarea,
        [data-baseweb="select"] > div,
        [data-baseweb="input"] {
            background-color: var(--input-bg) !important;
            color: var(--text) !important;
            border-color: var(--border) !important;
        }
        [data-testid="stChatInput"] {
            background-color: var(--input-bg) !important;
        }

        /* Buttons (secondary) */
        button[kind="secondary"],
        [data-testid="stBaseButton-secondary"] {
            background-color: var(--btn-bg) !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
        }
        button[kind="secondary"] p,
        [data-testid="stBaseButton-secondary"] p {
            color: var(--text) !important;
        }

        /* Expanders, chat messages, metrics, alerts, file uploader */
        [data-testid="stExpander"],
        [data-testid="stChatMessage"],
        [data-testid="stMetric"],
        [data-testid="stFileUploader"] section {
            background-color: var(--card) !important;
            border: 1px solid var(--border) !important;
            color: var(--text) !important;
        }
        [data-testid="stMetricValue"],
        [data-testid="stMetricLabel"] {
            color: var(--text) !important;
        }

        /* Tables / dataframes */
        [data-testid="stTable"], [data-testid="stDataFrame"] {
            background-color: var(--card) !important;
            color: var(--text) !important;
        }
        """

    css += "</style>"
    st.markdown(css, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
def _current_run_id():
    """Unique id of the current script run (None if unavailable)."""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        ctx = get_script_run_ctx()
        return getattr(ctx, "script_run_id", None)
    except Exception:
        return None


def _on_dark_toggle():
    # Runs BEFORE the script reruns, so the new theme applies immediately
    st.session_state["dark_mode"] = st.session_state["sb_dark_toggle"]


def render_sidebar(current_page="Home"):
    # Theme must be applied on every run, even if the sidebar is skipped below
    apply_theme()

    # Draw the sidebar only once PER RUN (not once per session).
    # Using the run id means the sidebar comes back correctly after st.rerun().
    run_id = _current_run_id()
    if run_id is not None:
        if st.session_state.get("_sidebar_run_id") == run_id:
            return
        st.session_state["_sidebar_run_id"] = run_id

    with st.sidebar:
        user_name, user_email = get_current_user()

        # 1. Branding Header
        st.markdown("""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 11px; background: #2563eb; color: white; padding: 2px 10px; border-radius: 12px; font-weight: 700;">ENTERPRISE</span>
                <span style="font-size: 11px; color: #10b981; font-weight: 700;">● Active</span>
            </div>
            <div style="font-size: 18px; font-weight: 800; color: var(--text); margin-bottom: 12px;">
                🤖 Adaptive Multi-Agent RAG
            </div>
        """, unsafe_allow_html=True)

        # 2. User Profile Card
        st.markdown(f"""
            <div style="background: var(--card-grad); border: 1px solid var(--border); padding: 12px 14px; border-radius: 12px; margin-bottom: 14px;">
                <div style="font-weight: 700; font-size: 14px; color: var(--accent);">👤 {user_name}</div>
                <div style="font-size: 11px; color: var(--muted);">{user_email}</div>
                <div style="font-size: 10px; color: var(--accent-soft); margin-top: 4px; font-weight: 600;">NMR Engineering College • Batch 05</div>
            </div>
        """, unsafe_allow_html=True)

        # 3. Theme Control (the only place this toggle is created)
        st.toggle(
            "🌙 Dark Mode",
            value=st.session_state.get("dark_mode", False),
            key="sb_dark_toggle",
            on_change=_on_dark_toggle,
        )

        st.markdown("---")

        # 4. Navigation Menu Bar (8 Pages)
        st.markdown("### 🧭 Navigation Menu")
        nav_items_meta = [
            ("Home", "home", "🏠", "Overview & Metrics"),
            ("Upload Documents", "upload", "📁", "Ingest & Vectorize"),
            ("Chat", "chat", "💬", "Multi-Agent Console"),
            ("Compare Documents", "compare", "⚖️", "Corpus Diff & Benchmarks"),
            ("Knowledge Graph", "graph", "🕸️", "Entity-Relation Graph"),
            ("Settings", "settings", "⚙️", "Account & Logout"),
            ("Memory", "memory", "🧠", "Documents, Key Points & Resources"),
            ("History", "history", "📜", "Your Past Questions"),
        ]

        current_active = st.session_state.get("page", "home").lower()
        if current_active in ("dashboard",):
            current_active = "chat"

        for label, page_key, icon, desc in nav_items_meta:
            is_active = (current_active == page_key)
            btn_label = f"{icon} {label}" + ("  ◀" if is_active else "")
            btn_type = "primary" if is_active else "secondary"
            if st.button(btn_label, key=f"sb_nav_btn_{page_key}", type=btn_type, use_container_width=True, help=desc):
                st.session_state["page"] = page_key
                st.session_state["nav_selection"] = label
                st.rerun()

        st.markdown("---")

        # 5. Multi-Agent RAG Controls Sidebar
        chat_sidebar()

        st.markdown("---")
        st.caption("🌓 v2.4 Enterprise RAG • Online")


__all__ = ["render_sidebar", "apply_theme"]