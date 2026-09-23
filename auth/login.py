import streamlit as st
from auth.user_db import verify_user

def login_page():
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.subheader("?? Login to Enterprise Multi-Agent RAG")
    with col_b:
        if st.button("?? Sign Up", use_container_width=True):
            st.session_state["auth_mode"] = "Signup"
            st.session_state["auth_page"] = "Signup"
            st.session_state["page"] = "Signup"
            st.rerun()

    with st.form("login_form"):
        user_input = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if not user_input or not password:
                st.warning("Please enter your credentials.")
            else:
                is_valid, user = verify_user(user_input, password)
                if is_valid:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = user
                    st.success(f"Welcome back, {user}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
