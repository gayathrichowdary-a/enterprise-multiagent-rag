import streamlit as st

from auth.database import get_connection
from auth.auth_utils import hash_password


def signup_page():

    st.title("📝 Create Account")

    full_name = st.text_input("Full Name")

    username = st.text_input("Username")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Create Account"):

        if (
            full_name == ""
            or username == ""
            or email == ""
            or password == ""
        ):
            st.error("Please fill all fields.")
            return

        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username=? OR email=?
            """,
            (
                username,
                email
            )
        )

        if cursor.fetchone():

            st.error(
                "Username or Email already exists."
            )

            conn.close()

            return

        hashed_password = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users
            (
                full_name,
                username,
                email,
                password
            )

            VALUES
            (
                ?,?,?,?
            )
            """,
            (
                full_name,
                username,
                email,
                hashed_password
            )
        )

        conn.commit()

        conn.close()

        st.success("Account Created Successfully!")

        st.session_state.page = "login"

        st.rerun()

    st.write("Already have an account?")

    if st.button("Login"):

        st.session_state.page = "login"

        st.rerun()