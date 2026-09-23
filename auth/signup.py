import streamlit as st
from auth.user_db import create_user

def signup_page():
    # Tab / Switch navigation
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.subheader("?? Create a New Account")
    with col_b:
        if st.button("?? Back to Login", use_container_width=True):
            st.session_state["auth_mode"] = "Login"
            st.session_state["auth_page"] = "Login"
            st.session_state["page"] = "Login"
            st.rerun()

    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        confirm_pw = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up", use_container_width=True)
        
        if submit:
            if not username or not email or not password:
                st.warning("Please fill out all fields.")
            elif password != confirm_pw:
                st.error("Passwords do not match.")
            else:
                success, msg = create_user(username, email, password)
                if success:
                    st.success("Account created successfully! Click 'Back to Login' above to sign in.")
                    st.session_state["auth_mode"] = "Login"
                    st.session_state["auth_page"] = "Login"
                    st.session_state["page"] = "Login"
                else:
                    st.error(msg)

    st.markdown("---")
    st.caption("Already registered? Click the **Back to Login** button at the top right.")
