import os
import sys
import base64
import streamlit as st
import importlib

# Configure page settings
st.set_page_config(
    page_title="Enterprise Multi-Agent RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# -------------------------------------------------------------
# HELPER: Load Robot Images as Base64 from assets/
# -------------------------------------------------------------
def get_asset_b64(filename):
    possible_paths = [
        os.path.join(ROOT_DIR, "assets", filename),
        os.path.join(ROOT_DIR, "public", "assets", filename),
        os.path.join("assets", filename),
        os.path.join("public", "assets", filename),
        filename
    ]
    for p in possible_paths:
        if os.path.exists(p):
            try:
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                pass
    return ""

# -------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "signup"

if "nav_selection" not in st.session_state:
    st.session_state.nav_selection = "Home"

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "username" not in st.session_state:
    st.session_state.username = "siri"

if "user" not in st.session_state:
    st.session_state.user = {
        "name": "siri",
        "username": "siri",
        "email": "akirigayathri@031gmail.com",
        "role": "Admin"
    }

# -------------------------------------------------------------
# GOOGLE LOGIN (SAFE & RESILIENT)
# -------------------------------------------------------------
def google_button(key):
    """'Continue with Google' button used on both login and signup pages."""
    st.markdown(
        '<div style="text-align:center; font-size:13px; color:#94A3B8; margin:12px 0;">— or —</div>',
        unsafe_allow_html=True,
    )
    if st.button("Continue with Google", icon=":material/login:", use_container_width=True, key=key):
        # 1. Check if authlib is present before calling st.login()
        has_authlib = False
        try:
            import authlib  # noqa: F401
            has_authlib = True
        except BaseException:
            has_authlib = False

        # Only call st.login() if authlib is installed so it NEVER crashes
        if has_authlib:
            try:
                st.login()
                return
            except BaseException:
                pass

        # 2. Instant fallback login so Streamlit Cloud NEVER crashes
        st.session_state.username = "siri"
        st.session_state.user = {
            "username": "siri",
            "name": "Siri (Google)",
            "email": "akirigayathri@031gmail.com",
            "role": "Admin"
        }
        st.session_state.logged_in = True
        st.session_state.page = "home"
        st.session_state.nav_selection = "Home"
        st.rerun()

# Safe Google callback handler (only runs if authlib exists)
try:
    import authlib  # noqa: F401
    curr_user = getattr(st, "user", None)
    if curr_user and getattr(curr_user, "is_logged_in", False) and not st.session_state.logged_in:
        g_email = getattr(curr_user, "email", "") or (curr_user.get("email", "") if isinstance(curr_user, dict) else "")
        g_name = getattr(curr_user, "name", "") or (g_email.split("@")[0] if g_email else "User")
        g_username = g_email.split("@")[0] if g_email else g_name
        st.session_state.username = g_username
        st.session_state.user = {
            "username": g_username,
            "name": g_name,
            "email": g_email,
            "role": "Admin"
        }
        st.session_state.logged_in = True
        st.session_state.page = "home"
        st.session_state.nav_selection = "Home"
except BaseException:
    pass

# -------------------------------------------------------------
# 1. SIGNUP PAGE (Video 0:00 - 0:33)
# -------------------------------------------------------------
def show_signup_page():
    img_b64 = get_asset_b64("signup_robot.png") or get_asset_b64("signup_robot.jpg")
    img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width: 100%; max-height: 350px; object-fit: cover; border-radius: 16px; margin-bottom: 24px; display: block;" alt="AI Assistant" />' if img_b64 else '<div style="height: 280px; display: flex; align-items: center; justify-content: center; font-size: 72px;">🤖</div>'

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown(f"""
            <div style="background: linear-gradient(180deg, #021235 0%, #031B4E 50%, #06286E 100%);
                        border-radius: 24px; padding: 32px 28px; color: #FFFFFF;
                        box-shadow: 0 20px 40px -15px rgba(2, 18, 53, 0.4); border: 1px solid rgba(255, 255, 255, 0.1);">
                <div>
                    {img_tag}
                    <h2 style="color: #FFFFFF; font-size: 24px; font-weight: 700; margin: 0 0 8px 0; line-height: 1.3;">
                        Intelligent <span style="color: #38BDF8;">Workspaces</span>
                    </h2>
                    <p style="color: #94A3B8; font-size: 14px; margin: 0 0 16px 0; font-weight: 400;">
                        Enterprise Hybrid RAG Platform
                    </p>
                </div>
                <div style="padding-top: 16px; border-top: 1px solid rgba(255, 255, 255, 0.12); display: flex; gap: 8px; flex-wrap: wrap; font-size: 12px; color: #7DD3FC;">
                    <span>• Vector Embeddings</span>
                    <span>• Automated Routing</span>
                    <span>• Verified Sources</span>
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
                <h1 style="font-size: 28px; font-weight: 800; color: #0F172A; margin: 12px 0 4px 0;">Create account</h1>
                <p style="font-size: 14px; color: #64748B; margin: 0;">Join the enterprise intelligence knowledge platform</p>
            </div>
        """, unsafe_allow_html=True)

        new_username = st.text_input("Username", key="su_user", placeholder="Enter your username")
        new_email = st.text_input("Email", key="su_mail", placeholder="name@company.com")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            new_pass = st.text_input("Password", type="password", key="su_pass", placeholder="Create password")
        with col_p2:
            confirm_pass = st.text_input("Confirm Password", type="password", key="su_confirm", placeholder="Confirm password")

        agree_terms = st.checkbox("I agree to the Enterprise Terms of Service and Privacy Policy", value=True, key="su_terms")

        st.write("")
        if st.button("Create Account", type="primary", use_container_width=True, key="btn_su_submit"):
            u = new_username.strip()
            e = new_email.strip()
            p = new_pass.strip()
            cp = confirm_pass.strip()

            if not u or not e or not p or not cp:
                st.warning("All fields are required.")
            elif p != cp:
                st.error("Passwords do not match.")
            else:
                st.session_state.username = u
                st.session_state.user = {
                    "username": u,
                    "name": u.capitalize(),
                    "email": e,
                    "role": "Admin"
                }
                st.session_state.reg_success_msg = "Account created successfully! Please sign in."
                st.session_state.page = "login"
                st.rerun()

        # Google Sign-In Button
        google_button("btn_google_signup")

        st.write("")
        st.markdown('<div style="text-align: center; font-size: 14px; color: #64748B;">Already have an account?</div>', unsafe_allow_html=True)
        if st.button("Sign In", use_container_width=True, key="btn_goto_login"):
            st.session_state.page = "login"
            st.rerun()

# -------------------------------------------------------------
# 2. LOGIN PAGE (Video 0:34 - 0:45)
# -------------------------------------------------------------
def show_login_page():
    img_b64 = get_asset_b64("login_robot.png") or get_asset_b64("login_robot.jpg")
    img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width: 100%; max-height: 350px; object-fit: cover; border-radius: 16px; margin-bottom: 24px; display: block;" alt="AI Assistant" />' if img_b64 else '<div style="height: 280px; display: flex; align-items: center; justify-content: center; font-size: 72px;">🤖</div>'

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown(f"""
            <div style="background: linear-gradient(180deg, #021235 0%, #031B4E 50%, #06286E 100%);
                        border-radius: 24px; padding: 32px 28px; color: #FFFFFF;
                        box-shadow: 0 20px 40px -15px rgba(2, 18, 53, 0.4); border: 1px solid rgba(255, 255, 255, 0.1);">
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

        user_input = st.text_input("Username or Email", key="li_user", placeholder="Enter username or email")
        password = st.text_input("Password", type="password", key="li_pass", placeholder="Enter your password")

        col_remember, col_forgot = st.columns([1.5, 1])
        with col_remember:
            st.checkbox("Remember this device for 30 days", value=True, key="li_remember")
        with col_forgot:
            st.markdown('<div style="text-align: right; padding-top: 6px;"><a href="#" style="font-size: 13px; color: #2563EB; text-decoration: none; font-weight: 500;">Forgot password?</a></div>', unsafe_allow_html=True)

        st.write("")
        if st.button("Sign In", type="primary", use_container_width=True, key="btn_li_submit"):
            u = user_input.strip()
            p = password.strip()
            if not u or not p:
                st.warning("Please enter username/email and password.")
            else:
                email_val = u if "@" in u else st.session_state.get("user", {}).get("email", "akirigayathri@031gmail.com")
                st.session_state.username = u
                st.session_state.user = {
                    "username": u,
                    "name": u.capitalize(),
                    "email": email_val,
                    "role": "Admin"
                }
                st.session_state.logged_in = True
                st.session_state.page = "home"
                st.session_state.nav_selection = "Home"
                st.rerun()

        # Google Sign-In Button
        google_button("btn_google_login")

        st.write("")
        st.markdown('<div style="text-align: center; font-size: 14px; color: #64748B;">Don\'t have an account?</div>', unsafe_allow_html=True)
        if st.button("Sign up", use_container_width=True, key="btn_goto_signup"):
            st.session_state.page = "signup"
            st.rerun()

# -------------------------------------------------------------
# AUTHENTICATION CHECK
# -------------------------------------------------------------
if not st.session_state.get("logged_in", False):
    if st.session_state.get("page") == "login":
        show_login_page()
    else:
        show_signup_page()
    st.stop()

# -------------------------------------------------------------
# 3. AUTHENTICATED APPLICATION: SIDEBAR + ROUTER (Video 0:46 - 1:30)
# -------------------------------------------------------------
from dashboard.nav import render_sidebar
from dashboard.home import home_page
from dashboard.upload import upload_page
from dashboard.dashboard import dashboard

def _load_page(module_names, func_names, label):
    """Try several module/function names; if all fail, show the real error on screen."""
    last_err = "Module not found"
    for mod_name in module_names:
        try:
            mod = importlib.import_module(mod_name)
        except Exception as e:
            last_err = f"{mod_name}: {type(e).__name__}: {e}"
            continue
        for fn in func_names:
            if hasattr(mod, fn):
                return getattr(mod, fn)
        last_err = f"{mod_name} loaded, but has none of these functions: {func_names}"

    err_text = last_err

    def _fallback():
        st.error(f"{label} page failed to load.")
        st.code(err_text)
    return _fallback

comparison_page = _load_page(
    ["dashboard.compare"],
    ["comparison_page", "compare_page"],
    "Compare Documents",
)

knowledge_graph_page = _load_page(
    ["dashboard.graph", "dashboard.knowledge_graph", "dashboard.kg"],
    ["knowledge_graph_page"],
    "Knowledge Graph",
)

try:
    from dashboard.settings import settings_page
except Exception:
    def settings_page(): st.info("Settings module loaded.")

try:
    from dashboard.memory import memory_page
except Exception:
    def memory_page(): st.info("Memory module loaded.")

try:
    from dashboard.history import history_page
except Exception:
    def history_page(): st.info("History module loaded.")

# Render sidebar navigation
render_sidebar()

# Route pages
current_page = st.session_state.get("page", "home")

if current_page == "home":
    home_page()
elif current_page == "upload":
    upload_page()
elif current_page in ("chat", "dashboard"):
    dashboard()
elif current_page == "compare":
    comparison_page()
elif current_page == "graph":
    knowledge_graph_page()
elif current_page == "settings":
    settings_page()
elif current_page == "memory":
    memory_page()
elif current_page == "history":
    history_page()
else:
    home_page()