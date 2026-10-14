import html

import streamlit as st
from dashboard.user_info import get_current_user


def _html(block: str) -> str:
    """Strip indentation and blank lines so Markdown never treats the HTML as a code block."""
    return "\n".join(line.strip() for line in block.splitlines() if line.strip())


def _field(label: str, value: str) -> str:
    return (
        '<div style="margin-bottom:14px;">'
        f'<div style="font-size:12px; font-weight:600; color:var(--muted); margin-bottom:4px; text-transform:uppercase; letter-spacing:0.4px;">{html.escape(label)}</div>'
        f'<div style="background:var(--input-bg); border:1px solid var(--border); border-radius:8px; padding:10px 14px; color:var(--text); font-size:15px;">{html.escape(str(value))}</div>'
        '</div>'
    )


def settings_page():
    st.title("⚙️ Settings")
    st.caption("Manage your account details and session.")

    name, email = get_current_user()
    u = st.session_state.get("user")
    if not isinstance(u, dict):
        u = {}
    username = u.get("username") or st.session_state.get("username") or "-"
    role = u.get("role", "User")

    safe_name = html.escape(str(name))
    safe_email = html.escape(str(email or "-"))
    safe_role = html.escape(str(role))
    initial = html.escape(str(name).strip()[:1].upper() or "U")

    # ---- Profile header card ----
    st.markdown(_html(f"""
        <div style="display:flex; align-items:center; gap:18px; background: var(--card-grad); border:1px solid var(--border); border-radius:16px; padding:20px 24px; margin: 8px 0 20px 0;">
        <div style="width:64px; height:64px; border-radius:50%; background:#2563eb; color:#ffffff; display:flex; align-items:center; justify-content:center; font-size:28px; font-weight:800; flex-shrink:0;">{initial}</div>
        <div style="flex:1; min-width:0;">
        <div style="font-size:22px; font-weight:800; color:var(--text);">{safe_name}</div>
        <div style="font-size:13px; color:var(--muted); margin-top:2px;">{safe_email}</div>
        </div>
        <span style="font-size:11px; font-weight:700; letter-spacing:0.5px; background:rgba(37,99,235,0.15); color:var(--accent-soft); border:1px solid var(--accent-soft); padding:4px 12px; border-radius:999px; text-transform:uppercase;">{safe_role}</span>
        </div>
    """), unsafe_allow_html=True)

    # ---- Account information (read-only cards, no disabled inputs) ----
    with st.container(border=True):
        st.markdown("#### 👤 Account Information")
        st.caption("These details are managed by your administrator and can't be edited here.")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(_field("Display name", name) + _field("Email", email or "-"), unsafe_allow_html=True)
        with c2:
            st.markdown(_field("Username", username) + _field("Role", role), unsafe_allow_html=True)

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    # ---- Session ----
    with st.container(border=True):
        st.markdown("#### 🔐 Session")
        st.caption("Signing out clears your session on this device.")

        if st.button("🚪 Logout", key="settings_logout_btn", type="primary"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.session_state["logged_in"] = False
            st.rerun()


__all__ = ["settings_page"]