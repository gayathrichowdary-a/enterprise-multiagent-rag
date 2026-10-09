import streamlit as st
import base64
import os
from auth.database import create_user

def get_image_base64(filepath):
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

def signup_page():
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none; }
        .block-container {
            max-width: 1080px !important;
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }
        div.stButton > button:first-child {
            background-color: #2563EB;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            border: none;
            width: 100%;
            transition: all 0.2s;
        }
        div.stButton > button:first-child:hover {
            background-color: #1D4ED8;
            color: white;
            border: none;
        }
        .secondary-btn button {
            background-color: #FFFFFF !important;
            color: #334155 !important;
            border: 1px solid #CBD5E1 !important;
            font-weight: 500 !important;
        }
        .secondary-btn button:hover {
            background-color: #F8FAFC !important;
            color: #0F172A !important;
            border-color: #94A3B8 !important;
        }
        .link-btn button {
            background: none !important;
            border: none !important;
            color: #2563EB !important;
            font-weight: 600 !important;
            padding: 0 !important;
            display: inline !important;
            width: auto !important;
            text-decoration: underline;
        }
        </style>
    """, unsafe_allow_html=True)

    img_b64 = get_image_base64("assets/signup_robot.jpg")
    img_tag = f'<img src="data:image/jpeg;base64,{img_b64}" style="width: 100%; border-radius: 14px; box-shadow: 0 12px 30px rgba(0,0,0,0.35);">' if img_b64 else '<img src="https://ais-dev-ju234xxwta5uivor2mhblf-88157110275.asia-southeast1.run.app/signup_robot.jpg" style="width: 100%; border-radius: 14px; box-shadow: 0 12px 30px rgba(0,0,0,0.35);">'

    col_left, col_right = st.columns([1, 1], gap="large")

    # ================= LEFT DARK BLUE CARD =================
    with col_left:
        st.markdown(f"""
            <div style="background-color: #031B4E; border-radius: 20px; padding: 36px 32px; height: 100%; display: flex; flex-direction: column; justify-content: space-between; border: 1px solid rgba(59,130,246,0.25);">
                <div style="text-align: center; margin-bottom: 24px;">
                    {img_tag}
                </div>
                <div>
                    <h2 style="color: #FFFFFF; font-size: 26px; font-weight: 800; line-height: 1.25; margin: 0 0 8px 0;">
                        Join Enterprise RAG
                    </h2>
                    <p style="color: #93C5FD; font-size: 13.5px; line-height: 1.45; margin: 0;">
                        Get started with your account and explore trusted, AI-powered insights for your organization.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ================= RIGHT WHITE CARD =================
    with col_right:
        st.markdown("""
            <div style="padding: 10px 10px 0 10px;">
                <div style="display: flex; items-center; gap: 10px; margin-bottom: 4px;">
                    <span style="font-size: 28px;">🧠</span>
                    <span style="font-size: 24px; font-weight: 700; color: #0F172A; line-height: 34px;">Enterprise RAG</span>
                </div>
                <p style="color: #64748B; font-size: 14px; margin: 0 0 20px 0;">
                    Create your account to get started.
                </p>
            </div>
        """, unsafe_allow_html=True)

        full_name = st.text_input("Full name", placeholder="Full name", key="signup_name", label_visibility="collapsed")
        email = st.text_input("Email address", placeholder="Email address", key="signup_email", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="Password", key="signup_pass", label_visibility="collapsed")
        confirm_pass = st.text_input("Confirm password", type="password", placeholder="Confirm password", key="signup_confirm", label_visibility="collapsed")

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        if st.button("Create Account", type="primary", use_container_width=True):
            if not full_name.strip() or not email.strip() or not password.strip() or not confirm_pass.strip():
                st.error("Please fill in all fields.")
            elif password != confirm_pass:
                st.error("Passwords do not match.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                success, msg = create_user(full_name, email, password)
                if success:
                    st.session_state.reg_success = msg
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error(msg)

        # Divider OR
        st.markdown("""
            <div style="text-align: center; margin: 18px 0; position: relative;">
                <hr style="border: none; border-top: 1px solid #E2E8F0; margin: 0;">
                <span style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: white; padding: 0 12px; color: #94A3B8; font-size: 12px; font-weight: 600;">OR</span>
            </div>
        """, unsafe_allow_html=True)

        # Continue with Google button
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("🌐 Continue with Google", key="google_signup", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.user = {"username": "Google User", "email": "user@enterprise.com", "id": 1}
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Switch to Login
        st.markdown("""
            <div style="text-align: center; margin-top: 24px; font-size: 13.5px; color: #64748B;">
                Already have an account?
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="link-btn" style="text-align: center;">', unsafe_allow_html=True)
        if st.button("Log in", key="switch_to_login"):
            st.session_state.page = "login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)