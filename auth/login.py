import os
import streamlit as st
from auth.database import verify_user

# High-resolution AI Assistant banner fallback URL
BANNER_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1200&auto=format&fit=crop"

def login_page():
    # Outer container for centered split-card layout
    _, col_main, _ = st.columns([0.05, 0.9, 0.05])
    
    with col_main:
        # Card wrapper
        col_banner, col_form = st.columns([1.1, 1], gap="large")

        # --- LEFT COLUMN: AI ROBOT BANNER ---
        with col_banner:
            # Check for local image first, then fallback to high-tech banner
            local_img_path = os.path.join("assets", "auth_banner.jpg")
            if os.path.exists(local_img_path):
                st.image(local_img_path, use_container_width=True)
            else:
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #09132b 0%, #10214d 60%, #1e1b4b 100%);
                                border-radius: 16px; padding: 36px 28px; text-align: center; color: white;
                                border: 1px solid #1e3a8a; box-shadow: 0 10px 25px rgba(0,0,0,0.3); margin-bottom: 12px;">
                        <div style="font-size: 5rem; line-height: 1; margin-bottom: 12px;">🤖</div>
                        <div style="display: inline-flex; gap: 8px; margin-bottom: 14px;">
                            <span style="background: rgba(56, 189, 248, 0.15); border: 1px solid #38bdf8; color: #38bdf8; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">📄 Docs</span>
                            <span style="background: rgba(34, 197, 94, 0.15); border: 1px solid #22c55e; color: #22c55e; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">🗄️ SQL/Vector</span>
                            <span style="background: rgba(168, 85, 247, 0.15); border: 1px solid #a855f7; color: #a855f7; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">🛡️ Guardrails</span>
                        </div>
                        <h2 style="font-weight: 800; font-size: 1.5rem; margin-bottom: 6px; color: #ffffff;">Smarter Answers.<br/>Trusted Sources.</h2>
                        <p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.4; margin: 0 auto; max-width: 320px;">
                            AI-powered multi-agent RAG for enterprise knowledge management and reliable grounded reasoning.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            # Feature points beneath the banner
            st.markdown("""
                <div style="display: flex; flex-direction: column; gap: 8px; padding: 0 8px;">
                    <div style="display: flex; align-items: center; gap: 10px; font-size: 0.82rem; color: #475569;">
                        <span style="color: #2563eb; font-weight: 700;">✓</span> 8-Node LangGraph self-correcting agent workflow
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px; font-size: 0.82rem; color: #475569;">
                        <span style="color: #2563eb; font-weight: 700;">✓</span> Real-time Faithfulness and Grounded citations
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px; font-size: 0.82rem; color: #475569;">
                        <span style="color: #2563eb; font-weight: 700;">✓</span> Persistent vector memory and query tracking
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # --- RIGHT COLUMN: LOGIN FORM ---
        with col_form:
            # Registration success toast notification
            if st.session_state.get("reg_success_msg"):
                st.success(st.session_state.pop("reg_success_msg"))

            with st.container(border=True):
                # Header branding
                st.markdown("""
                    <div style="text-align: left; padding: 10px 0 16px 0;">
                        <div style="display: inline-block; background: #eff6ff; color: #2563eb; font-size: 0.75rem; font-weight: 700; padding: 3px 10px; border-radius: 6px; margin-bottom: 8px;">
                            ENTERPRISE PORTAL
                        </div>
                        <h2 style="margin: 0; font-size: 1.6rem; font-weight: 800; color: #0f172a;">Sign In</h2>
                        <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.88rem;">
                            Log in to access your intelligent knowledge platform
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                # Form input fields
                username_input = st.text_input(
                    "Username or Email",
                    key="login_identity",
                    placeholder="Enter your username or email"
                )
                password_input = st.text_input(
                    "Password",
                    type="password",
                    key="login_secret",
                    placeholder="Enter your password"
                )

                st.write("")
                login_btn = st.button("🚀 Sign In", type="primary", use_container_width=True)

                if login_btn:
                    if not username_input or not password_input:
                        st.error("⚠️ Please provide both username/email and password.")
                    else:
                        with st.spinner("Authenticating credentials..."):
                            user_data = verify_user(username_input, password_input)
                            if user_data:
                                # Save user object to session state
                                st.session_state["user"] = user_data
                                st.session_state["logged_in"] = True
                                st.session_state["user_id"] = user_data.get("id", 1) if isinstance(user_data, dict) else 1
                                st.session_state["username"] = user_data.get("username", username_input) if isinstance(user_data, dict) else username_input
                                st.success("Authentication successful! Redirecting...")
                                st.rerun()
                            else:
                                st.error("❌ Invalid username/email or password. Please try again.")

                # Divider & Switch to Signup
                st.markdown("""
                    <div style="text-align: center; margin: 18px 0 12px 0; position: relative;">
                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 0;"/>
                        <span style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: white; padding: 0 10px; font-size: 0.75rem; color: #94a3b8; font-weight: 600;">OR</span>
                    </div>
                """, unsafe_allow_html=True)

                if st.button("Create New Account", use_container_width=True):
                    st.session_state["auth_page"] = "signup"
                    st.rerun()
