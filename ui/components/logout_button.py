"""
Logout button component for MindEase.
"""

import streamlit as st

from ui.navigation import navigate
from utils.session import logout_session


def logout_button():
    """Display the logout button."""

    if st.sidebar.button("🚪 Logout"):

        logout_session()

        navigate("landing")