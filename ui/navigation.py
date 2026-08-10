"""
Navigation utilities for MindEase.
"""

import streamlit as st


def initialize_navigation():
    """
    Initialize application navigation state.
    """

    # ---------------------------------------------------------
    # Initialize login state if it does not exist
    # ---------------------------------------------------------

    if "logged_in" not in st.session_state:

        st.session_state.logged_in = False

    # ---------------------------------------------------------
    # Initialize user ID
    # ---------------------------------------------------------

    if "user_id" not in st.session_state:

        st.session_state.user_id = None

    # ---------------------------------------------------------
    # Initialize page
    # ---------------------------------------------------------

    if "page" not in st.session_state:

        if st.session_state.logged_in:

            st.session_state.page = "dashboard"

        else:

            st.session_state.page = "landing"


def navigate(page_name: str):
    """
    Switch to another page.
    """

    st.session_state.page = page_name

    st.rerun()