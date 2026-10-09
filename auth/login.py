import os
import base64
import streamlit as st
from auth.database import verify_user

def get_login_image_b64():
    """Prioritizes your local assets folder image."""
    possible_paths = [
        "assets/login_robot.png",
        "assets/login_robot.jpg",
        "assets/image.png",
        "assets/login.png",
        "assets/login.jpg",
        "assets/robot.png",
        "assets/robot.jpg",
        "login_robot.png",
        "login_robot.jpg",
    ]
    for p in possible_paths:
        if os.path.exists(p):
            try:
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                pass
    return ""

def login_page():
    # Inject CSS for smooth scrolling and responsive layout
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"] {
            overflow-y: auto !important;
            height: 100% !important;
        }
        .main .block-container {
            max-width: 1050px !important;
            padding-top: 2rem !important;
            padding-bottom: 4rem !important;
            overflow: visible !important;
        }
        div[data-testid="stToolbar"] {
            visibility: hidden;
            height: 0%;
            position: fixed;
        }
        .stTextInput > div > div > input {
            border-radius: 8px !important;
            border: 1px solid #E2E8F0 !important;
            padding: 10px 14px !important;
            font-size: 14px !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #2563EB !important;
            box-shadow: 0 0 0 1px #2563EB !important;
        }
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.6rem 1rem !important;
            font-size: 15px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    img_b64 = get_login_image_b64()

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width: 100%; max-height: 350px; object-fit: cover; border-radius: 16px; margin-bottom: 24px; display: block;" alt="AI Assistant" />' if img_b64 else '<div style="height: 280px; display: flex; align-items: center; justify-content: center; font-size: 72px;">🤖</div>'

        st.markdown(f"""
            <div style="background: linear-gradient(180deg, #021235 0%, #031B4E 50%, #06286E 100%);
                        border-radius: 24px; padding: 32px 28px; color: #FFFFFF;
                        box-shadow: 0 20px 40px -15px rgba(2, 18, 53, 0.4); border: 1px solid rgba(255, 255, 255, 0.1);
                        display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    {img_tag}
                    <h2 style="color: #FFFFFF; font-size: 24px; font-weight: 700; margin: 0 0 8px 0; line-height: 1.3;">
                        Smarter Answers, <span style="color: #38BDF8;">Faster Insights</span>
                    </h2>
                    <p style="color: #94A3B8; font-size: 14px; margin: 0 0 16px 0; font-weight: 400;">
                        Enterprise Hybrid RAG Platform
                    </p>
                </div>
                <div style="padding-top: 16px; border-top: 1px solid rgba(255, 255, 255, 0.12); display: flex; gap: 8px; flex-wrap: wrap; font-size: 12px; color: #7DD3FC;">
                    <span>• Agentic Retrieval</span>
                    <span>• Reranking</span>
                    <span>• Multi-Vector Search</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
            <div style="margin-bottom: 20px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                    <div style="background: #2563EB; width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; font-weight: bold; box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);">
                        ⚡
                    </div>
                    <div>
                        <div style="font-weight: 800; font-size: 18px; color: #0F172A; line-height: 1.1;">Enterprise RAG</div>
                        <div style="font-size: 11px; color: #64748B;">Adaptive Intelligence Knowledge Platform</div>
                    </div>
                </div>
                <h1 style="font-size: 28px; font-weight: 800; color: #0F172A; margin: 12px 0 4px 0;">Welcome back</h1>
                <p style="font-size: 14px; color: #64748B; margin: 0;">Enter your credentials to access your enterprise workspace</p>
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.get("reg_success_msg"):
            st.success(st.session_state.pop("reg_success_msg"))

        user_input = st.text_input("Username or Email", key="login_username_input", placeholder="Enter username or email")
        password = st.text_input("Password", type="password", key="login_password_input", placeholder="Enter your password")

        col_remember, col_forgot = st.columns([1.5, 1])
        with col_remember:
            st.checkbox("Remember this device for 30 days", value=True, key="login_remember")
        with col_forgot:
            st.markdown('<div style="text-align: right; padding-top: 6px;"><a href="#" style="font-size: 13px; color: #2563EB; text-decoration: none; font-weight: 500;">Forgot password?</a></div>', unsafe_allow_html=True)

        st.write("")
        if st.button("Sign In", type="primary", use_container_width=True, key="btn_login_submit"):
            u_clean = user_input.strip()
            p_clean = password.strip()

            if not u_clean or not p_clean:
                st.warning("Please enter your username/email and password.")
            else:
                is_valid, username = verify_user(u_clean, p_clean)
                if is_valid:
                    email_addr = u_clean if "@" in u_clean else f"{username}@company.com"
                    st.session_state.user = {
                        "username": username,
                        "name": username.capitalize(),
                        "full_name": username.capitalize(),
                        "email": email_addr,
                        "role": "Admin"
                    }
                    st.session_state.username = username
                    st.session_state.logged_in = True
                    st.session_state.page = "home"
                    st.rerun()
                else:
                    st.error("Invalid username/email or password.")

        st.write("")
        st.markdown('<div style="text-align: center; font-size: 14px; color: #64748B;">Don\'t have an account?</div>', unsafe_allow_html=True)
        if st.button("Sign up", use_container_width=True, key="btn_goto_signup"):
            st.session_state.page = "signup"
            st.rerun()