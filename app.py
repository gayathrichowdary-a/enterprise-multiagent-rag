import os
import sys
import streamlit as st

# Ensure repository root is always in sys.path for Streamlit Cloud & local run
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure wide layout and page identity
st.set_page_config(
    page_title="Adaptive Multi-Agent RAG | Enterprise",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Safe imports for authentication pages
try:
    from auth.login import login_page
except Exception as e:
    def login_page():
        st.error(f"Error loading login page: {e}")

try:
    from auth.signup import signup_page
except Exception as e:
    def signup_page():
        st.error(f"Error loading signup page: {e}")

# Safe imports for dashboard pages
try:
    from dashboard.home import home_page
except Exception as e:
    def home_page():
        st.error(f"Error loading home page: {e}")

try:
    from dashboard.dashboard import dashboard
except Exception as e:
    def dashboard():
        st.error(f"Error loading dashboard: {e}")

try:
    from dashboard.upload import upload_page
except Exception as e:
    def upload_page():
        st.error(f"Error loading upload page: {e}")

try:
    from dashboard.compare import compare_page
except Exception as e:
    def compare_page():
        st.error(f"Error loading compare page: {e}")

try:
    from dashboard.graph import knowledge_graph_page
except Exception as e:
    def knowledge_graph_page():
        st.error(f"Error loading knowledge graph page: {e}")

try:
    from dashboard.settings import settings_page
except Exception as e:
    def settings_page():
        st.error(f"Error loading settings page: {e}")

try:
    from dashboard.memory import memory_page
except Exception as e:
    def memory_page():
        st.error(f"Error loading memory page: {e}")

try:
    from dashboard.history import history_page
except Exception as e:
    def history_page():
        st.error(f"Error loading history page: {e}")

# Initialize user authentication & navigation session states
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "nav_selection" not in st.session_state:
    st.session_state.nav_selection = "Home"

# Application Router
if st.session_state.logged_in:
    current_page = st.session_state.get("page", "dashboard")
    current_nav = st.session_state.get("nav_selection", "Home")

    if current_page == "home" or current_nav == "Home":
        home_page()
    elif current_page == "upload" or current_nav == "Upload Documents":
        upload_page()
    elif current_page == "compare" or current_nav == "Compare Documents":
        compare_page()
    elif current_page == "graph" or current_nav == "Knowledge Graph":
        knowledge_graph_page()
    elif current_page == "settings" or current_nav == "Settings":
        settings_page()
    elif current_page == "memory" or current_nav == "Memory":
        memory_page()
    elif current_page == "history" or current_nav == "History":
        history_page()
    else:
        # Default to interactive multi-agent chat console
        dashboard()
else:
    if st.session_state.page == "signup":
        signup_page()
    else:
        login_page()
