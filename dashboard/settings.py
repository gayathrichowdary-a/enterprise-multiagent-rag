import streamlit as st
from dashboard.user_info import get_current_user


def settings_page():
    st.title("⚙️ Settings")
    st.caption("Your account details.")

    name, email = get_current_user()
    u = st.session_state.get("user")
    if not isinstance(u, dict):
        u = {}
    username = u.get("username") or st.session_state.get("username") or "-"
    role = u.get("role", "User")

    st.markdown(f"### 👤 {name}")

    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Display name", value=name, disabled=True, key="set_name")
        st.text_input("Email", value=email or "-", disabled=True, key="set_email")
    with c2:
        st.text_input("Username", value=username, disabled=True, key="set_username")
        st.text_input("Role", value=role, disabled=True, key="set_role")

    st.markdown("---")

    if st.button("🚪 Logout", key="settings_logout_btn", type="primary"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.session_state["logged_in"] = False
        st.rerun()