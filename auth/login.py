# auth/login.py
import streamlit as st
from auth.database import get_user_by_username
from auth.auth_utils import verify_password
from database.profile_memory import load_profile_memory

def login_page():
    st.markdown("""
        <style>
        /* Modern Single Card Styling */
        .login-card {
            background-color: #ffffff;
            padding: 2.2rem;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.02);
            margin-top: 2rem;
            text-align: center;
        }
        .brand-badge {
            display: inline-block;
            background: #eff6ff;
            color: #2563eb;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 0.6rem;
        }
        .login-header {
            font-size: 1.85rem;
            font-weight: 700;
            color: #0f172a;
            margin: 0;
            letter-spacing: -0.02em;
        }
        .login-subtext {
            font-size: 0.9rem;
            color: #64748b;
            margin-top: 0.3rem;
            margin-bottom: 1.5rem;
        }
        div.stButton > button:first-child {
            border-radius: 10px;
            font-weight: 600;
            font-size: 0.95rem;
            padding: 0.6rem 1.2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Centering columns
    col_left, col_center, col_right = st.columns([1, 1.2, 1])

    with col_center:
        # Top Card Header
        st.markdown("""
            <div class="login-card">
                <span class="brand-badge">🛡️ Enterprise Access</span>
                <h1 class="login-header">🔐 Login</h1>
                <p class="login-subtext">Adaptive Multi-Agent Knowledge Platform</p>
            </div>
        """, unsafe_allow_html=True)

        st.write("") # small spacing

        # Login Form
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="e.g. gayathri", key="login_user")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
            
            st.write("")
            submit = st.form_submit_button("Login", use_container_width=True, type="primary")

            if submit:
                if not username.strip() or not password.strip():
                    st.warning("⚠️ Please provide both username and password.")
                else:
                    user = get_user_by_username(username.strip())
                    if user:
                        # user: (id, full_name, username, email, password, created_at)
                        stored_hash = user[4]
                        if verify_password(password, stored_hash):
                            st.session_state.logged_in = True
                            st.session_state.user = {
                                "id": user[0],
                                "full_name": user[1],
                                "name": user[1],
                                "username": user[2],
                                "email": user[3]
                            }
                            st.session_state.user_profile = load_profile_memory(user[0])
                            st.session_state.page = "dashboard"
                            st.toast(f"Welcome back, {user[1]}! 👋", icon="✅")
                            st.rerun()
                        else:
                            st.error("❌ Invalid password. Please check your credentials.")
                    else:
                        st.error("❌ Account not found with that username.")

        st.markdown("<div style='text-align: center; margin-top: 1rem;'>", unsafe_allow_html=True)
        st.caption("Don't have an account?")
        if st.button("Create Account", use_container_width=True):
            st.session_state.page = "signup"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)