import streamlit as st
from auth.user_db import verify_user

def login_page():
    # Centered modern card layout
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown('''
            <div style="text-align: center; padding: 20px 0 10px 0;">
                <h2 style="margin-bottom: 4px; font-weight: 700; color: #1E293B;">Enterprise Multi-Agent RAG</h2>
                <p style="color: #64748B; font-size: 14px; margin-top: 0;">Sign in to access your intelligent knowledge platform</p>
            </div>
        ''', unsafe_allow_html=True)
        
        if st.session_state.get("reg_success_msg"):
            st.success(st.session_state.pop("reg_success_msg"))

        with st.container(border=True):
            st.markdown("<h4 style='margin-bottom: 16px; color: #334155;'>Sign In</h4>", unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=False):
                user_identity = st.text_input("Username or Email", placeholder="Enter your username or email")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                submit = st.form_submit_button("Sign In", use_container_width=True, type="primary")
                
                if submit:
                    if not user_identity or not password:
                        st.warning("Please fill in both fields.")
                    else:
                        is_valid, user = verify_user(user_identity, password)
                        if is_valid:
                            st.session_state["authenticated"] = True
                            st.session_state["username"] = user
                            st.session_state["email"] = user_identity if "@" in user_identity else f"{user}@domain.com"
                            st.rerun()
                        else:
                            st.error("Invalid username/email or password.")

        st.markdown("<div style='text-align: center; margin-top: 16px;'>", unsafe_allow_html=True)
        st.write("Don't have an account yet?")
        if st.button("Create an Account", use_container_width=True):
            st.session_state["auth_page"] = "signup"
            st.session_state["auth_mode"] = "signup"
            st.session_state["page"] = "signup"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
