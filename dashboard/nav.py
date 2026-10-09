import streamlit as st
from dashboard.chat import chat_sidebar

def render_sidebar(current_page="Home"):
    with st.sidebar:
        user_obj = st.session_state.get("user", {})
        user_name = user_obj.get("name") or st.session_state.get("user_name") or "Ahemaraju Siri"
        user_email = user_obj.get("email") or st.session_state.get("user_email") or "siri@enterprise.ai"

        # 1. Branding Header
        st.markdown("""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 11px; background: #2563eb; color: white; padding: 2px 10px; border-radius: 12px; font-weight: 700;">ENTERPRISE</span>
                <span style="font-size: 11px; color: #10b981; font-weight: 700;">● Active</span>
            </div>
            <div style="font-size: 18px; font-weight: 800; color: #1e293b; margin-bottom: 12px;">
                🤖 Adaptive Multi-Agent RAG
            </div>
        """, unsafe_allow_html=True)

        # 2. User Profile Card
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%); border: 1px solid #bfdbfe; padding: 12px 14px; border-radius: 12px; margin-bottom: 14px;">
                <div style="font-weight: 700; font-size: 14px; color: #1e3a8a;">👤 {user_name}</div>
                <div style="font-size: 11px; color: #64748b;">{user_email}</div>
                <div style="font-size: 10px; color: #3b82f6; margin-top: 4px; font-weight: 600;">NMR Engineering College • Batch 05</div>
            </div>
        """, unsafe_allow_html=True)

        # 3. Theme & Logout Controls
        is_dark = st.session_state.get("dark_mode", False)
        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            dark_toggle = st.toggle("🌙 Dark Mode", value=is_dark, key="sb_dark_toggle")
            if dark_toggle != is_dark:
                st.session_state["dark_mode"] = dark_toggle
                st.rerun()
        with col_t2:
            if st.button("Logout", key="sb_logout_btn", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["page"] = "login"
                st.rerun()

        st.markdown("---")

        # 4. Navigation Menu Bar (8 Pages)
        st.markdown("### 🧭 Navigation Menu")
        nav_items_meta = [
            ("Home", "home", "🏠", "Overview & Metrics"),
            ("Upload Documents", "upload", "📁", "Ingest & Vectorize"),
            ("Chat", "chat", "💬", "Multi-Agent Console"),
            ("Compare Documents", "compare", "⚖️", "Corpus Diff & Benchmarks"),
            ("Knowledge Graph", "graph", "🕸️", "Entity-Relation Graph"),
            ("Settings", "settings", "⚙️", "Agent & Model Configs"),
            ("Memory", "memory", "🧠", "Episodic Working Buffer"),
            ("History", "history", "📜", "Execution Traces & Audit")
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

__all__ = ["render_sidebar"]