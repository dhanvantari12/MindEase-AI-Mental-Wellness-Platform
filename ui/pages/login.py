"""
Login page for MindEase.
"""

import streamlit as st

from features.auth.services import login_user
from ui.navigation import navigate
from utils.session import login_session


def show_login_page():
    """Display the login page."""

    st.title("👋 Welcome Back")
    st.caption("Continue your wellness journey.")

    # Show success message after signup
    if st.session_state.get("signup_success"):
        st.success("🎉 Account created successfully! Please login.")
        st.session_state.signup_success = False

    # Email input
    email = st.text_input(
        "📧 Email",
        placeholder="Enter your email",
    )

    # Password input
    password = st.text_input(
        "🔒 Password",
        type="password",
        placeholder="Enter your password",
    )

    st.write("")

    # Login button
    if st.button("Login", use_container_width=True):

        # Temporary debug
        st.write("Email entered:", repr(email))
        st.write("Password length:", len(password))

        success, message, user = login_user(
            email=email.strip(),
            password=password,
        )

        if success:
            login_session(user)
            st.success("🎉 Login Successful!")
            navigate("dashboard")
        else:
            st.error(message)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back"):
            navigate("landing")

    with col2:
        if st.button("Create Account"):
            navigate("signup")