import os
import streamlit as st
from auth.database import register_user

def signup_page():
    # Outer container for centered split-card layout
    _, col_main, _ = st.columns([0.05, 0.9, 0.05])

    with col_main:
        col_banner, col_form = st.columns([1.1, 1], gap="large")

        # --- LEFT COLUMN: MATCHING BRAND BANNER ---
        with col_banner:
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
                        <h2 style="font-weight: 800; font-size: 1.5rem; margin-bottom: 6px; color: #ffffff;">Join Enterprise RAG</h2>
                        <p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.4; margin: 0 auto; max-width: 320px;">
                            Set up your account in seconds to index enterprise docs, execute agentic queries, and track accuracy.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("""
                <div style="display: flex; flex-direction: column; gap: 8px; padding: 0 8px;">
                    <div style="display: flex; align-items: center; gap: 10px; font-size: 0.82rem; color: #475569;">
                        <span style="color: #2563eb; font-weight: 700;">✓</span> Unlimited document uploads (.pdf, .docx, .txt)
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px; font-size: 0.82rem; color: #475569;">
                        <span style="color: #2563eb; font-weight: 700;">✓</span> Dedicated personal memory and learning partition
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px; font-size: 0.82rem; color: #475569;">
                        <span style="color: #2563eb; font-weight: 700;">✓</span> Role-based enterprise security and session encryption
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # --- RIGHT COLUMN: SIGNUP FORM ---
        with col_form:
            with st.container(border=True):
                st.markdown("""
                    <div style="text-align: left; padding: 10px 0 16px 0;">
                        <div style="display: inline-block; background: #ecfdf5; color: #059669; font-size: 0.75rem; font-weight: 700; padding: 3px 10px; border-radius: 6px; margin-bottom: 8px;">
                            GET STARTED FREE
                        </div>
                        <h2 style="margin: 0; font-size: 1.6rem; font-weight: 800; color: #0f172a;">Create Account</h2>
                        <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.88rem;">
                            Enter your details to register for the platform
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                new_username = st.text_input("Username", key="reg_user", placeholder="e.g. jdoe")
                new_email = st.text_input("Work Email", key="reg_email", placeholder="e.g. jdoe@enterprise.com")
                new_password = st.text_input("Password", type="password", key="reg_pwd", placeholder="Minimum 6 characters")
                confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_pwd", placeholder="Re-type password")

                st.write("")
                submit_signup = st.button("✨ Create Account", type="primary", use_container_width=True)

                if submit_signup:
                    if not new_username or not new_email or not new_password or not confirm_password:
                        st.error("⚠️ Please fill in all fields.")
                    elif len(new_password) < 6:
                        st.error("⚠️ Password must be at least 6 characters.")
                    elif new_password != confirm_password:
                        st.error("⚠️ Passwords do not match.")
                    else:
                        with st.spinner("Creating your account..."):
                            try:
                                success = register_user(new_username, new_email, new_password)
                            except TypeError:
                                # In case register_user only expects (username, password)
                                success = register_user(new_username, new_password)

                            if success:
                                st.session_state["reg_success_msg"] = f"🎉 Account for '{new_username}' created successfully! Please sign in."
                                st.session_state["auth_page"] = "login"
                                st.rerun()
                            else:
                                st.error("❌ Username or email already exists. Please pick another.")

                # Divider & Switch back to Login
                st.markdown("""
                    <div style="text-align: center; margin: 18px 0 12px 0; position: relative;">
                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 0;"/>
                        <span style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: white; padding: 0 10px; font-size: 0.75rem; color: #94a3b8; font-weight: 600;">ALREADY REGISTERED?</span>
                    </div>
                """, unsafe_allow_html=True)

                if st.button("Already have an account? Sign In", use_container_width=True):
                    st.session_state["auth_page"] = "login"
                    st.rerun()
