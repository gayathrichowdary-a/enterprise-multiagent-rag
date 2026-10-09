import streamlit as st
from dashboard.upload import document_sidebar
from dashboard.chat import chat_sidebar

def render_sidebar(current_page="Home"):
    """
    Renders the unified enterprise sidebar matching the user's complete navigation structure:
    - ENTERPRISE status badge & Adaptive Multi-Agent RAG branding
    - User Profile Card with User Name, Email, and college badge
    - Dark mode toggle & Logout
    - Navigation Buttons/Menu:
        1. Home
        2. Upload Documents
        3. Chat
        4. Compare Documents
        5. Knowledge Graph
        6. Settings
        7. Memory
        8. History
    - Document Management & Multi-Agent RAG Controls
    """
    with st.sidebar:
        user_obj = st.session_state.get("user", {})
        user_name = user_obj.get("name") or st.session_state.get("user_name") or st.session_state.get("username") or "Siri"
        user_email = user_obj.get("email") or st.session_state.get("user_email") or "siri@enterprise.ai"

        # 1. Branding Header
        st.markdown("""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 11px; background: #2563eb; color: white; padding: 2px 10px; border-radius: 12px; font-weight: 700; letter-spacing: 0.5px;">ENTERPRISE</span>
                <span style="font-size: 11px; color: #10b981; font-weight: 700;">● Active</span>
            </div>
            <div style="font-size: 18px; font-weight: 800; color: #1e293b; margin-bottom: 12px; line-height: 1.2;">
                🤖 Adaptive Multi-Agent RAG
            </div>
        """, unsafe_allow_html=True)

        # 2. User Profile Card
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%); border: 1px solid #bfdbfe; padding: 12px 14px; border-radius: 12px; margin-bottom: 14px;">
                <div style="font-weight: 700; font-size: 14px; color: #1e3a8a;">👤 {user_name}</div>
                <div style="font-size: 11px; color: #64748b; word-break: break-all;">{user_email}</div>
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
                st.session_state["authenticated"] = False
                st.session_state["page"] = "login"
                st.session_state["nav_selection"] = "Home"
                st.session_state.pop("user", None)
                st.rerun()

        st.markdown("---")

        # 4. Navigation Menu Bar with full button set requested by user
        st.markdown("### 🧭 Navigation")
        nav_options = [
            "Home",
            "Upload Documents",
            "Chat",
            "Compare Documents",
            "Knowledge Graph",
            "Settings",
            "Memory",
            "History"
        ]

        # Ensure nav_selection state is valid
        if "nav_selection" not in st.session_state or st.session_state["nav_selection"] not in nav_options:
            st.session_state["nav_selection"] = current_page if current_page in nav_options else "Home"

        current_nav_index = nav_options.index(st.session_state["nav_selection"]) if st.session_state["nav_selection"] in nav_options else 0

        selected_nav = st.radio(
            "Navigation Menu",
            nav_options,
            index=current_nav_index,
            key="radio_nav_menu",
            label_visibility="collapsed"
        )

        if selected_nav != st.session_state["nav_selection"]:
            st.session_state["nav_selection"] = selected_nav
            # Synchronize page router key
            page_map = {
                "Home": "home",
                "Upload Documents": "upload",
                "Chat": "dashboard",
                "Compare Documents": "compare",
                "Knowledge Graph": "graph",
                "Settings": "settings",
                "Memory": "memory",
                "History": "history"
            }
            st.session_state["page"] = page_map.get(selected_nav, "dashboard")
            st.rerun()

        st.markdown("---")

        # 5. Document Management Sidebar (Uploads & Indexing)
        document_sidebar()

        st.markdown("---")

        # 6. Multi-Agent RAG Controls Sidebar
        chat_sidebar()

__all__ = ["render_sidebar"]
