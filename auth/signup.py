import streamlit as st
from auth.user_db import create_user

def signup_page():
    st.subheader("Create a New Account")
    
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        confirm_pw = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")
        
        if submit:
            if not username or not email or not password:
                st.warning("Please fill out all fields.")
            elif password != confirm_pw:
                st.error("Passwords do not match.")
            else:
                success, msg = create_user(username, email, password)
                if success:
                    st.success("Account created successfully! You can now log in.")
                else:
                    st.error(msg)
