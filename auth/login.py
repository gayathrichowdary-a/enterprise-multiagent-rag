import streamlit as st
from auth.user_db import verify_user

def login_page():
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown('''
            <div style="text-align: center; padding: 20px 0 10px 0;">
                <h2 style="margin-bottom: 4px; font-weight: 700; color: #1E293B;">Enterprise Multi-Agent RAG</h2>
                <p style="color: #64748B; font-size: 14px; margin-top: 0;">Log in to access your intelligent knowledge platform</p>
            </div>
        ''', unsafe_allow_html=True)
        
        if st.session_state.get("reg_success_msg"):
            st.success(st.session_state.pop("reg_success_msg"))

        with st.container(border=True):
            st.markdown("<h3 style='margin-bottom: 20px; color: #1E293B; text-align: center;'>Login</h3>", unsafe_allow_html=True)
            
            # Using direct inputs with keys to prevent form desync
            user_identity = st.text_input("Username or Email", key="login_identity_input", placeholder="Enter your username or email")
            password = st.text_input("Password", type="password", key="login_password_input", placeholder="Enter your password")
            
            st.write("")
            login_clicked = st.button("Login", use_container_width=True, type="primary")
            
            if login_clicked:
                clean_user = user_identity.strip()
                clean_pass = password.strip()
                
                if not clean_user or not clean_pass:
                    st.warning("Please fill in both fields.")
                else:
                    is_valid, user = verify_user(clean_user, clean_pass)
                    if is_valid:
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = user
                        st.session_state["email"] = clean_user if "@" in clean_user else f"{user}@domain.com"
                        st.success(f"Welcome back, {user}!")
                        st.rerun()
                    else:
                        st.error("Invalid username/email or password.")

        st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
        st.write("Don't have an account yet?")
        if st.button("Create an Account", use_container_width=True):
            st.session_state["auth_page"] = "signup"
            st.session_state["auth_mode"] = "signup"
            st.session_state["page"] = "signup"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
