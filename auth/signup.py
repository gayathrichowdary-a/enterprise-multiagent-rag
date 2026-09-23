import streamlit as st
from auth.user_db import create_user

def signup_page():
    col_head, col_btn = st.columns([3, 1])
    with col_head:
        st.subheader("Create a New Account")
    with col_btn:
        if st.button("Back to Login", use_container_width=True):
            st.session_state["auth_mode"] = "Login"
            st.session_state["auth_page"] = "Login"
            st.session_state["page"] = "Login"
            st.rerun()

    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up", use_container_width=True)
        
        if submit:
            if not username or not email or not password:
                st.warning("All fields are required.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success, msg = create_user(username, email, password)
                if success:
                    st.success("Account created successfully! Click 'Back to Login' above to sign in.")
                else:
                    st.error(msg)
