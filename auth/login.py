import streamlit as st
from auth.user_db import verify_user

def login_page():
    col_head, col_btn = st.columns([3, 1])
    with col_head:
        st.subheader("Login to Enterprise Multi-Agent RAG")
    with col_btn:
        if st.button("Sign Up", use_container_width=True):
            st.session_state["auth_mode"] = "Signup"
            st.session_state["auth_page"] = "Signup"
            st.session_state["page"] = "Signup"
            st.rerun()

    with st.form("login_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if not (username or email) or not password:
                st.warning("Please enter your username/email and password.")
            else:
                user_key = username if username else email
                is_valid, user = verify_user(user_key, password)
                if is_valid:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = user
                    st.success(f"Welcome back, {user}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please check your username and password.")
