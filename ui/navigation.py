import streamlit as st


def initialize_navigation():
    """Initialize page state."""
    if "page" not in st.session_state:
        st.session_state.page = "landing"

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user_id" not in st.session_state:
        st.session_state.user_id = None


def navigate(page_name: str):
    """Switch to another page."""
    st.session_state.page = page_name
    st.rerun()