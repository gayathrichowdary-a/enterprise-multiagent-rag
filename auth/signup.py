import streamlit as st
from auth.user_db import create_user

def signup_page():
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown('''
            <div style="text-align: center; padding: 20px 0 10px 0;">
                <h2 style="margin-bottom: 4px; font-weight: 700; color: #1E293B;">Enterprise Multi-Agent RAG</h2>
                <p style="color: #64748B; font-size: 14px; margin-top: 0;">Create your account to start querying enterprise data</p>
            </div>
        ''', unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("<h3 style='margin-bottom: 20px; color: #1E293B; text-align: center;'>Create Account</h3>", unsafe_allow_html=True)
            
            username = st.text_input("Username", key="reg_username", placeholder="e.g. jdoe")
            email = st.text_input("Email", key="reg_email", placeholder="name@company.com")
            password = st.text_input("Password", type="password", key="reg_password", placeholder="Enter password")
            re_password = st.text_input("Re-enter Password", type="password", key="reg_re_password", placeholder="Confirm your password")
            
            st.write("")
            if st.button("Create Account", use_container_width=True, type="primary"):
                u = username.strip()
                e = email.strip()
                p = password.strip()
                rp = re_password.strip()
                
                if not u or not e or not p or not rp:
                    st.warning("All fields are required.")
                elif p != rp:
                    st.error("Passwords do not match.")
                else:
                    success, msg = create_user(u, e, p)
                    if success:
                        st.session_state["reg_success_msg"] = "Account created successfully! You can now log in."
                        st.session_state["auth_page"] = "login"
                        st.session_state["auth_mode"] = "login"
                        st.session_state["page"] = "login"
                        st.rerun()
                    else:
                        st.error(msg)

        st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
        st.write("Already have an account?")
        if st.button("Back to Login", use_container_width=True):
            st.session_state["auth_page"] = "login"
            st.session_state["auth_mode"] = "login"
            st.session_state["page"] = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
