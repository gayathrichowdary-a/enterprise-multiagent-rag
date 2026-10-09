import streamlit as st
import base64
import os
from auth.database import verify_user

def get_image_base64(filepath):
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

def login_page():
    # Hide Streamlit default chrome & style widgets
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

    img_b64 = get_image_base64("assets/login_robot.jpg")
    img_tag = f'<img src="data:image/jpeg;base64,{img_b64}" style="width: 100%; border-radius: 14px; box-shadow: 0 12px 30px rgba(0,0,0,0.35);">' if img_b64 else '<img src="https://ais-dev-ju234xxwta5uivor2mhblf-88157110275.asia-southeast1.run.app/login_robot.jpg" style="width: 100%; border-radius: 14px; box-shadow: 0 12px 30px rgba(0,0,0,0.35);">'

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
                        Smarter Answers.<br>
                        <span style="color: #60A5FA;">Trusted Sources.</span>
                    </h2>
                    <p style="color: #93C5FD; font-size: 13.5px; line-height: 1.45; margin: 0;">
                        AI-powered multi-agent RAG for enterprise knowledge management.
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
                    Login to access your enterprise knowledge and get trusted answers.
                </p>
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.get("reg_success"):
            st.success(st.session_state.pop("reg_success"))

        email_input = st.text_input("Email address", placeholder="Email address", key="login_email", label_visibility="collapsed")
        pass_input = st.text_input("Password", type="password", placeholder="Password", key="login_password", label_visibility="collapsed")

        # Remember me / Forgot password row
        opt_col1, opt_col2 = st.columns([1, 1])
        with opt_col1:
            remember_me = st.checkbox("Remember me", value=True)
        with opt_col2:
            st.markdown('<div style="text-align: right; padding-top: 5px;"><a href="#" style="color: #2563EB; font-size: 13px; text-decoration: none; font-weight: 500;">Forgot password?</a></div>', unsafe_allow_html=True)

        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

        if st.button("Login", type="primary", use_container_width=True):
            if not email_input.strip() or not pass_input.strip():
                st.error("Please enter both email/username and password.")
            else:
                is_valid, user_name, user_email = verify_user(email_input, pass_input)
                if is_valid:
                    st.session_state.logged_in = True
                    st.session_state.user = {
                        "username": user_name,
                        "email": user_email or email_input,
                        "id": 1
                    }
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

        # Divider OR
        st.markdown("""
            <div style="text-align: center; margin: 18px 0; position: relative;">
                <hr style="border: none; border-top: 1px solid #E2E8F0; margin: 0;">
                <span style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: white; padding: 0 12px; color: #94A3B8; font-size: 12px; font-weight: 600;">OR</span>
            </div>
        """, unsafe_allow_html=True)

        # Continue with Google button
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("🌐 Continue with Google", key="google_login", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.user = {"username": "Google User", "email": "user@enterprise.com", "id": 1}
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Switch to Signup
        st.markdown("""
            <div style="text-align: center; margin-top: 24px; font-size: 13.5px; color: #64748B;">
                Don't have an account?
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="link-btn" style="text-align: center;">', unsafe_allow_html=True)
        if st.button("Sign up", key="switch_to_signup"):
            st.session_state.page = "signup"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)