"""
Signup page for MindEase.
"""

import streamlit as st

from features.auth.services import register_user
from ui.navigation import navigate


def show_signup_page():
    """Display the signup page."""

    st.title("🌸 Create Your Account")
    st.caption("Start your wellness journey today.")

    # User Inputs
    name = st.text_input(
        "👤 Full Name",
        placeholder="Enter your full name",
    )

    email = st.text_input(
        "📧 Email",
        placeholder="Enter your email",
    )

    password = st.text_input(
        "🔒 Password",
        type="password",
        placeholder="Create a strong password",
    )

    confirm_password = st.text_input(
        "🔒 Confirm Password",
        type="password",
        placeholder="Re-enter your password",
    )

    st.write("")

    # Create Account Button
    if st.button("🌸 Create Account", use_container_width=True):

        success, message = register_user(
            full_name=name.strip(),
            email=email.strip(),
            password=password,
            confirm_password=confirm_password,
        )

        if success:
            st.success("🎉 " + message)

            # Show success message on login page
            st.session_state.signup_success = True

            navigate("login")

        else:
            st.error(message)

    st.write("")

    # Back to Login
    if st.button("Already have an account? Login"):
        navigate("login")