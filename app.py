import streamlit as st
st.set_page_config(page_title="Adaptive Multi-Agent RAG", page_icon="🤖", layout="wide")
from auth.database import create_database
from auth.signup import signup_page
from auth.login import login_page
from dashboard.source_ranking import source_rankings_page
from dashboard.dashboard import dashboard
from dashboard.home import home_page
from dashboard.upload import upload_page
from dashboard.chat import chat_page
from dashboard.memory import memory_page
from dashboard.history import history_page
from dashboard.settings import settings_page
from dashboard.graph_view import knowledge_graph_page
from dashboard.comparison import comparison_page
# ==================================
# SECURITY CONFIG
# ==================================
create_database()

# ==================================
# SESSION STATE
# ==================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "vector_stores" not in st.session_state:
    st.session_state.vector_stores = {}

if "uploaded_documents" not in st.session_state:
    st.session_state.uploaded_documents = []

if "knowledge_sources" not in st.session_state:
    st.session_state.knowledge_sources = {}

# ==================================
# LOGIN CHECK (runs on every rerun, not just once)
# ==================================

if not st.session_state.logged_in:

    if st.session_state.page == "login":
        login_page()

    elif st.session_state.page == "signup":
        signup_page()

    st.stop()

# ===========================
# DASHBOARD NAVIGATION
# ===========================

selected_page = dashboard()

if selected_page == "🏠 Home":
    home_page()

elif selected_page == "📤 Upload Documents":
    upload_page()

elif selected_page == "💬 Chat":
    chat_page()
elif selected_page == "🕸️ Knowledge Graph":
    knowledge_graph_page()

elif selected_page == "⚖️ Compare Documents":
    comparison_page()       
elif selected_page == "📊 Source Rankings":
    source_rankings_page()  

elif selected_page == "🧠 Memory":
    memory_page()

elif selected_page == "📜 History":
    history_page()

elif selected_page == "⚙️ Settings":
    settings_page()

elif selected_page == "🚪 Logout":
    st.session_state.clear()
    st.rerun()