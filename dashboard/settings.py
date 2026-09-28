import streamlit as st

def settings_page():
    st.title("⚙️ Settings")

    user = st.session_state.get("user", {})
    if isinstance(user, str):
        full_name = user
        username = user.lower()
        email = f"{username}@system.ai"
    elif isinstance(user, dict):
        full_name = user.get("full_name") or user.get("name") or "Enterprise User"
        username = user.get("username") or user.get("name") or "enterprise_user"
        email = user.get("email") or "user@system.ai"
    else:
        full_name = "Enterprise User"
        username = "enterprise_user"
        email = "user@system.ai"

    st.subheader("👤 Account Profile")
    st.write(f"**Name:** {full_name}")
    st.write(f"**Username:** {username}")
    st.write(f"**Email:** {email}")

    st.divider()

    st.subheader("Session Controls")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()
