import streamlit as st

def settings_page():

    st.title("⚙️ Settings")

    user = st.session_state["user"]

    st.subheader("Account")

    st.write(f"**Name:** {user['full_name']}")
    st.write(f"**Username:** {user['username']}")
    st.write(f"**Email:** {user['email']}")

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.clear()

        st.rerun()