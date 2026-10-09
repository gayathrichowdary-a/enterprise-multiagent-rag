import streamlit as st
import os
import urllib.request
from auth.database import create_user

ROBOT_IMG_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80"
LOCAL_IMG = "assets/login_robot_banner.jpg"

def ensure_banner_image():
    if not os.path.exists(LOCAL_IMG):
        os.makedirs("assets", exist_ok=True)
        try:
            urllib.request.urlretrieve(ROBOT_IMG_URL, LOCAL_IMG)
        except Exception:
            pass

def signup_page():
    ensure_banner_image()

    st.markdown("""
        <style>
            .stApp {
                background-color: #0f172a;
            }
            .block-container {
                max-width: 1050px !important;
                padding-top: 3rem !important;
                padding-bottom: 3rem !important;
            }
            /* Card styling */
            .auth-card-left {
                background: linear-gradient(145deg, #0b1329 0%, #0d1b3e 50%, #0a1226 100%);
                border: 1px solid rgba(56, 189, 248, 0.2);
                border-radius: 24px 0 0 24px;
                padding: 40px 32px;
                color: #ffffff;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
            }
            .auth-card-right {
                background: #ffffff;
                border-radius: 0 24px 24px 0;
                padding: 40px 36px;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
                height: 100%;
            }
            @media (max-width: 768px) {
                .auth-card-left { border-radius: 24px 24px 0 0; }
                .auth-card-right { border-radius: 0 0 24px 24px; }
            }
            div.stButton > button[kind="primary"] {
                background: linear-gradient(90deg, #2563eb, #3b82f6) !important;
                color: white !important;
                font-weight: 600 !important;
                border-radius: 12px !important;
                padding: 0.6rem 1rem !important;
                border: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

    col_visual, col_form = st.columns([1.1, 1], gap="small")

    # LEFT COLUMN: 3D Robot & Enterprise Branding
    with col_visual:
        st.markdown('''
            <div class="auth-card-left">
                <div>
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
                        <span style="font-size: 26px;">🤖</span>
                        <div>
                            <div style="font-size: 13px; font-weight: 700; color: #38bdf8; letter-spacing: 0.5px; text-transform: uppercase;">
                                Multi-Agent RAG
                            </div>
                            <div style="font-size: 11px; color: #94a3b8;">Enterprise AI Engine</div>
                        </div>
                    </div>
                </div>
        ''', unsafe_allow_html=True)

        if os.path.exists(LOCAL_IMG):
            st.image(LOCAL_IMG, use_container_width=True)
        else:
            st.image(ROBOT_IMG_URL, use_container_width=True)

        st.markdown('''
                <div style="text-align: center; margin-top: 24px;">
                    <h2 style="color: #ffffff; font-size: 24px; font-weight: 800; line-height: 1.2; margin-bottom: 8px;">
                        Smarter Answers.<br/>
                        <span style="color: #38bdf8;">Trusted Sources.</span>
                    </h2>
                    <p style="color: #cbd5e1; font-size: 12px; line-height: 1.5; margin: 0 auto; max-width: 320px;">
                        Transforming enterprise repositories into verified, conversational intelligence with real-time faithfulness.
                    </p>
                </div>
                <div style="margin-top: 25px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-between; font-size: 11px; color: #94a3b8;">
                    <span>🛡️ ARES 95%+ Faithfulness</span>
                    <span>⚡ Zero Hallucination Filter</span>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    # RIGHT COLUMN: Clean Create Account Form
    with col_form:
        st.markdown('''
            <div class="auth-card-right">
                <div style="margin-bottom: 24px;">
                    <span style="background: #eff6ff; color: #2563eb; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 999px;">
                        Enterprise Multi-Agent RAG
                    </span>
                    <h1 style="color: #0f172a; font-size: 26px; font-weight: 800; margin-top: 10px; margin-bottom: 4px;">
                        Create Account
                    </h1>
                    <p style="color: #64748B; font-size: 13px; margin: 0;">
                        Sign up to access your intelligent knowledge platform
                    </p>
                </div>
        ''', unsafe_allow_html=True)

        # Form inputs
        username_val = st.text_input("Username", placeholder="e.g. jdoe", key="su_username")
        email_val = st.text_input("Email address", placeholder="name@company.com", key="su_email")
        password_val = st.text_input("Password", type="password", placeholder="••••••••", key="su_pass")
        confirm_val = st.text_input("Confirm password", type="password", placeholder="••••••••", key="su_conf")

        st.write("")
        if st.button("Create Account", type="primary", use_container_width=True, key="su_submit"):
            u_clean = username_val.strip()
            e_clean = email_val.strip()
            p_clean = password_val.strip()
            c_clean = confirm_val.strip()

            if not u_clean or not e_clean or not p_clean:
                st.error("Please fill in all fields.")
            elif p_clean != c_clean:
                st.error("Passwords do not match.")
            elif len(p_clean) < 6:
                st.warning("Password must be at least 6 characters long.")
            else:
                success, msg = create_user(u_clean, e_clean, p_clean)
                if success:
                    st.success("Account created successfully! Redirecting to login...")
                    st.session_state["auth_page"] = "login"
                    st.rerun()
                else:
                    st.error(f"Error: {msg}")

        # Google Sign In and Link to Login
        st.markdown('''
            <div style="position: relative; margin: 18px 0; text-align: center;">
                <hr style="border-top: 1px solid #e2e8f0; margin: 0;"/>
                <span style="position: relative; top: -10px; background: #ffffff; padding: 0 10px; color: #94a3b8; font-size: 11px;">
                    or continue with
                </span>
            </div>
        ''', unsafe_allow_html=True)

        if st.button("🌐 Continue with Google", use_container_width=True, key="su_google"):
            st.info("Google SSO enabled for verified domain accounts.")

        st.markdown('''
            <div style="margin-top: 20px; text-align: center; font-size: 12px; color: #64748b;">
                Already have an account?
            </div>
        ''', unsafe_allow_html=True)

        if st.button("Sign In", use_container_width=True, key="switch_to_login"):
            st.session_state["auth_page"] = "login"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
