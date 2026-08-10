"""
Login page for MindEase.
"""

import streamlit as st

from features.auth.services import login_user
from ui.navigation import navigate
from utils.session import login_session


def show_login_page():
    """Display the login page."""

    # ---------------------------------------------------------
    # Page Header
    # ---------------------------------------------------------

    st.title("👋 Welcome Back")

    st.caption(
        "Continue your wellness journey."
    )

    # ---------------------------------------------------------
    # Signup Success Message
    # ---------------------------------------------------------

    if st.session_state.get("signup_success"):

        st.success(
            "🎉 Account created successfully!"
        )

        st.info(
            "Please login using your email and password."
        )

        st.session_state.signup_success = False

    # ---------------------------------------------------------
    # Login Inputs
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Login Button
    # ---------------------------------------------------------

    if st.button(
        "Login",
        use_container_width=True,
    ):

        # -----------------------------------------------------
        # Clean Input
        # -----------------------------------------------------

        email = email.strip()

        # -----------------------------------------------------
        # Basic Validation
        # -----------------------------------------------------

        if not email:

            st.error(
                "Please enter your email."
            )

            return

        if not password:

            st.error(
                "Please enter your password."
            )

            return

        # -----------------------------------------------------
        # Authenticate User
        # -----------------------------------------------------

        success, message, user = login_user(
            email=email,
            password=password,
        )

        # -----------------------------------------------------
        # Successful Login
        # -----------------------------------------------------

        if success:

            # Creates both:
            # 1. Streamlit session
            # 2. Persistent browser session
            login_session(user)

            st.success(
                "🎉 Login successful!"
            )

            # Move to dashboard
            navigate("dashboard")

        # -----------------------------------------------------
        # Failed Login
        # -----------------------------------------------------

        else:

            st.error(message)

    st.write("")

    # ---------------------------------------------------------
    # Navigation Buttons
    # ---------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Back",
            use_container_width=True,
        ):

            navigate("landing")

    with col2:

        if st.button(
            "Create Account",
            use_container_width=True,
        ):

            navigate("signup")