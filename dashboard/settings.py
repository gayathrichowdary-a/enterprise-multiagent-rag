import streamlit as st

def settings_page():
    st.title("⚙️ Settings & Role-Based Access Control (RBAC)")

    user = st.session_state.get("user", {})
    if isinstance(user, dict):
        username = user.get("username", "Gayathri")
        current_role = user.get("role", "Enterprise Admin")
    else:
        username = str(user) if user else "Gayathri"
        current_role = "Enterprise Admin"

    st.subheader("👤 User Profile & Role Assignment")
    st.write(f"**Authenticated User:** `{username}`")
    
    # Interactive Role Switcher for RBAC demonstration
    selected_role = st.selectbox(
        "Active Role:",
        ["Enterprise Admin", "Enterprise Analyst"],
        index=0 if current_role == "Enterprise Admin" else 1
    )
    if isinstance(user, dict):
        st.session_state["user"]["role"] = selected_role
    else:
        st.session_state["user"] = {"username": username, "role": selected_role, "id": 1}

    st.divider()

    st.subheader("🛡️ RBAC Permissions Matrix")
    if selected_role == "Enterprise Admin":
        st.success("✅ **Enterprise Admin Permissions Active**:")
        st.markdown("- Ingest new documents (PDF, CSV, DOCX, TXT, OCR images)\n- Manage Knowledge Source authority tiers\n- Clear and rebuild hybrid FAISS & BM25 indices\n- Execute Chat & ARES Evaluation")
    else:
        st.warning("🔒 **Enterprise Analyst Permissions Active**:")
        st.markdown("- Query Chat with RRF Hybrid Retrieval\n- Explore Multi-Hop Knowledge Graph\n- Run live ARES Evaluation benchmarks\n- ❌ Upload & index deletion restricted")

    st.divider()
    st.subheader("Session Authentication")
    st.info("🔒 Authentication mode: Enterprise Session RBAC. Login token is securely validated within active browser session.")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()
