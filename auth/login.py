import os
import streamlit as st
from auth.database import verify_user, create_user

BANNER_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80"

def login_page():
    _, col_center, _ = st.columns([0.05, 0.9, 0.05])

    with col_center:
        col_banner, col_form = st.columns([1, 1], gap="medium")

        # --- LEFT: ROBOT BANNER ---
        with col_banner:
            local_banner = os.path.join("assets", "auth_banner.jpg")
            if os.path.exists(local_banner):
                st.image(local_banner, use_container_width=True)
            else:
                st.image(BANNER_URL, use_container_width=True)

            st.markdown("""
                <div style="background: #0f172a; padding: 18px; border-radius: 12px; border: 1px solid #1e293b; margin-top: 10px;">
                    <div style="display: flex; gap: 8px; margin-bottom: 10px;">
                        <span style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">📄 Docs</span>
                        <span style="background: rgba(34, 197, 94, 0.2); color: #22c55e; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">🗄️ SQL/Vector</span>
                        <span style="background: rgba(168, 85, 247, 0.2); color: #a855f7; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">🛡️ Guardrails</span>
                    </div>
                    <h3 style="color: white; margin: 0 0 6px 0; font-size: 1.15rem; font-weight: 700;">Smarter Answers. Trusted Sources.</h3>
                    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">AI-powered multi-agent RAG for enterprise knowledge management and reliable grounded reasoning.</p>
                </div>
                <div style="margin-top: 12px; display: flex; flex-direction: column; gap: 6px; font-size: 0.82rem; color: #64748b;">
                    <div>✓ 8-Node LangGraph self-correcting agent workflow</div>
                    <div>✓ Real-time Faithfulness and Grounded citations</div>
                    <div>✓ Persistent vector memory and query tracking</div>
                </div>
            """, unsafe_allow_html=True)

        # --- RIGHT: SIGN IN & CREATE ACCOUNT ---
        with col_form:
            with st.container(border=True):
                st.markdown("""
                    <div style="display: inline-block; background: #eff6ff; color: #2563eb; font-size: 0.75rem; font-weight: 700; padding: 3px 10px; border-radius: 6px; margin-bottom: 8px;">
                        ENTERPRISE PORTAL
                    </div>
                """, unsafe_allow_html=True)

                tab_signin, tab_signup = st.tabs(["🔑 Sign In", "✨ Create Account"])

                # --- 1. SIGN IN ---
                with tab_signin:
                    st.markdown("<h3 style='margin-bottom: 4px; color: #1e293b;'>Sign In</h3>", unsafe_allow_html=True)
                    st.caption("Log in to access your intelligent knowledge platform")

                    login_user = st.text_input("Username or Email", key="auth_signin_user", placeholder="Enter username or email")
                    login_pwd = st.text_input("Password", type="password", key="auth_signin_pwd", placeholder="Enter password")

                    st.write("")
                    if st.button("🚀 Sign In", type="primary", use_container_width=True, key="btn_signin"):
                        if not login_user or not login_pwd:
                            st.warning("⚠️ Please provide username/email and password.")
                        else:
                            # verify_user returns: (is_valid: bool, username: str or None)
                            is_valid, user_name = verify_user(login_user, login_pwd)
                            
                            if is_valid:
                                st.session_state["logged_in"] = True
                                st.session_state["user"] = {"username": user_name, "id": 1}
                                st.session_state["username"] = user_name
                                st.success(f"Welcome back, {user_name}! Loading...")
                                st.rerun()
                            else:
                                st.error("❌ Invalid username/email or password. If you don't have an account, click the 'Create Account' tab.")

                # --- 2. CREATE ACCOUNT ---
                with tab_signup:
                    st.markdown("<h3 style='margin-bottom: 4px; color: #1e293b;'>Create Account</h3>", unsafe_allow_html=True)
                    st.caption("Register a new account on the enterprise platform")

                    reg_user = st.text_input("Username", key="auth_reg_user", placeholder="e.g. jdoe")
                    reg_email = st.text_input("Work Email", key="auth_reg_email", placeholder="e.g. jdoe@enterprise.com")
                    reg_pwd = st.text_input("Password", type="password", key="auth_reg_pwd", placeholder="Minimum 6 characters")
                    reg_pwd_confirm = st.text_input("Confirm Password", type="password", key="auth_reg_confirm", placeholder="Re-type password")

                    st.write("")
                    if st.button("✨ Register Account", type="primary", use_container_width=True, key="btn_signup"):
                        if not reg_user or not reg_email or not reg_pwd:
                            st.warning("⚠️ All fields are required.")
                        elif reg_pwd != reg_pwd_confirm:
                            st.error("❌ Passwords do not match!")
                        elif len(reg_pwd) < 4:
                            st.error("❌ Password must be at least 4 characters.")
                        else:
                            # create_user returns: (is_created: bool, message: str)
                            is_created, msg = create_user(reg_user, reg_email, reg_pwd)
                            
                            if is_created:
                                st.success(f"🎉 {msg} Please switch to the 'Sign In' tab to log in.")
                            else:
                                st.error(f"❌ {msg}")
