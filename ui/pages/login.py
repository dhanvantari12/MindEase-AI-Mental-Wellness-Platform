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

    # Show signup success message
    if st.session_state.get("signup_success"):
        st.success("🎉 Account created successfully!")
        st.info("Please login using your email and password.")
        st.session_state.signup_success = False

    # Login inputs
    email = st.text_input(
        "📧 Email",
        placeholder="Enter your email",
        key="login_email",
    )

    password = st.text_input(
        "🔒 Password",
        type="password",
        placeholder="Enter your password",
        key="login_password",
    )

    st.write("")

    # Login button
    if st.button("Login", use_container_width=True):

        # Clean input
        email = email.strip()

        # Basic validation
        if not email:
            st.error("Please enter your email.")
            return

        if not password:
            st.error("Please enter your password.")
            return

        # Authenticate user
        success, message, user = login_user(
            email=email,
            password=password,
        )

        if success:
            # Store logged-in user
            login_session(user)

            # Mark login state
            st.session_state.logged_in = True
            st.session_state.user_id = str(user.id)
            st.session_state.user_name = user.full_name

            st.success("🎉 Login successful!")

            # Move to dashboard
            navigate("dashboard")

        else:
            st.error(message)

    st.write("")

    # Navigation buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back"):
            navigate("landing")

    with col2:
        if st.button("Create Account"):
            navigate("signup")