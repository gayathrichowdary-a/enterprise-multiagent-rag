import os
import sys
import traceback

import streamlit as st

# Make sure the project root is importable on Streamlit Cloud
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Must be the first Streamlit command
st.set_page_config(
    page_title="Enterprise Multi-Agent RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Imports (wrapped so the real error is shown instead of the redacted one)
try:
    from dashboard.nav import render_sidebar
    from dashboard.home import home_page
    from dashboard.upload import upload_page
    from dashboard.dashboard import dashboard
    from dashboard.comparison import comparison_page
    from dashboard.graph_view import knowledge_graph_page
    from dashboard.settings import settings_page
    from dashboard.memory import memory_page
    from dashboard.history import history_page
except Exception:
    st.error("Import error. Full traceback below:")
    st.code(traceback.format_exc())
    st.stop()

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

if "page" not in st.session_state:
    st.session_state.page = "home"

if "nav_selection" not in st.session_state:
    st.session_state.nav_selection = "Home"

# 1. Render Sidebar Navigation Once
render_sidebar()

# 2. Page Router
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