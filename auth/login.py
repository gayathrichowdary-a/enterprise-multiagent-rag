import streamlit as st
from auth.user_db import verify_user

def login_page():
    st.subheader("Login to Enterprise Multi-Agent RAG")
    
    with st.form("login_form"):
        user_input = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
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
