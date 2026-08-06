"""
Dashboard page.
"""

import streamlit as st
from ui.components.logout_button import logout_button
from utils.session import is_logged_in


def show_dashboard():

    if not is_logged_in():

        st.error("Please login first.")

        return

    st.title("🌸 MindEase Dashboard")

    logout_button()
    
    st.success(
        f"Welcome back, {st.session_state.user_name} 💙"
    )

    st.write("---")

    st.write("Dashboard coming soon...")
    