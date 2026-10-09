import os
import sys
import streamlit as st

# Ensure repository root is in sys.path for Streamlit Cloud
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="Enterprise Multi-Agent RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Safe imports for auth
try:
    from auth.login import login_page
except Exception as e:
    def login_page():
        st.error(f"Error loading login: {e}")

try:
    from auth.signup import signup_page
except Exception as e:
    def signup_page():
        st.error(f"Error loading signup: {e}")

# Safe imports for dashboard
try:
    from dashboard.dashboard import dashboard
except Exception as e:
    def dashboard():
        st.error(f"Error loading dashboard: {e}")

try:
    from dashboard.upload import upload_page
except Exception:
    # Safe fallback if upload_page doesn't exist
    def upload_page():
        dashboard()

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Router
if st.session_state.logged_in:
    if st.session_state.get("page") == "upload":
        upload_page()
    else:
        dashboard()
else:
    if st.session_state.page == "signup":
        signup_page()
    else:
        login_page()