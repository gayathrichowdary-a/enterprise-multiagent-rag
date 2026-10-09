import streamlit as st

st.set_page_config(
    page_title="Enterprise Multi-Agent RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

from dashboard.nav import render_sidebar
from dashboard.home import home_page
from dashboard.upload import upload_page
from dashboard.dashboard import dashboard
from dashboard.compare import compare_page
from dashboard.graph import knowledge_graph_page
from dashboard.settings import settings_page
from dashboard.memory import memory_page
from dashboard.history import history_page

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
    compare_page()
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