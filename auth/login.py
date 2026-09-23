import streamlit as st
from auth.database import verify_user

def login_page():
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown('''
            <div style="text-align: center; padding: 25px 0 10px 0;">
                <h2 style="margin-bottom: 4px; font-weight: 700; color: #1E293B;">Enterprise Multi-Agent RAG</h2>
                <p style="color: #64748B; font-size: 14px; margin-top: 0;">Log in to access your intelligent knowledge platform</p>
            </div>
        ''', unsafe_allow_html=True)
        
        if st.session_state.get("reg_success_msg"):
            st.success(st.session_state.pop("reg_success_msg"))

        with st.container(border=True):
            st.markdown("<h3 style='margin-bottom: 20px; color: #1E293B; text-align: center;'>Login</h3>", unsafe_allow_html=True)
            
            user_input = st.text_input("Username or Email", key="login_identity", placeholder="Enter username or email")
            password = st.text_input("Password", type="password", key="login_secret", placeholder="Enter password")
            
            st.write("")
            if st.button("Login", use_container_width=True, type="primary"):
                u_clean = user_input.strip()
                p_clean = password.strip()
                
                if not u_clean or not p_clean:
                    st.warning("Please enter your username/email and password.")
                else:
                    is_valid, user = verify_user(u_clean, p_clean)
                    if is_valid:
                        st.session_state.logged_in = True
                        st.session_state.username = user
                        st.session_state.user = user
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("Invalid username/email or password.")

        st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
        st.write("Don't have an account yet?")
        if st.button("Create an Account", use_container_width=True):
            st.session_state.page = "signup"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
