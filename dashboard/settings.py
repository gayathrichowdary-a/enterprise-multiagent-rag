import streamlit as st

def settings_page():
    st.title("⚙️ Settings & Governance")

    user = st.session_state.get("user", {})
    if isinstance(user, str):
        full_name = user
        username = user.lower()
        role = "Enterprise Admin" if "admin" in username else "Enterprise Analyst"
    elif isinstance(user, dict):
        full_name = user.get("full_name") or user.get("name") or "Gayathri"
        username = user.get("username") or user.get("name") or "enterprise_user"
        role = user.get("role", "Enterprise Admin" if "admin" in str(username).lower() else "Enterprise Analyst")
    else:
        full_name = "Gayathri"
        username = "enterprise_user"
        role = "Enterprise Admin"

    st.subheader("👤 Account Profile & RBAC")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Name:** {full_name}")
        st.write(f"**Username:** {username}")
    with col2:
        st.write(f"**Assigned Role:** `{role}`")
        st.write(f"**Authentication:** Secure Enterprise Session Authentication")

    st.divider()

    st.subheader("🛡️ Role-Based Access Controls (RBAC)")
    if "admin" in role.lower():
        st.success("✅ **Admin Privileges Active**: Knowledge base indexing, source deletion, and authority score adjustments enabled.")
    else:
        st.info("ℹ️ **Standard Analyst Role**: Read, Query, and Evaluation permissions enabled. Policy editing restricted.")

    st.divider()

    st.subheader("Session Controls")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()
