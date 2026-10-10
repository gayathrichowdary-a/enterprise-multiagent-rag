import streamlit as st

def get_current_user():
    """Return (name, email) of the logged-in user from any common session key."""
    s = st.session_state
    u = s.get("user")
    if isinstance(u, str):
        u = {"name": u}
    if not isinstance(u, dict):
        u = {}

    name = (
        u.get("full_name") or u.get("name") or u.get("username") or u.get("display_name")
        or s.get("user_name") or s.get("username") or s.get("full_name") or s.get("name")
    )
    email = (
        u.get("email") or u.get("user_email") or u.get("mail")
        or s.get("user_email") or s.get("email")
    )
    return name or "User", email or ""