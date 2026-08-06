"""
Session management utilities for MindEase.
"""

import streamlit as st


def login_session(user):
    """
    Store logged-in user information.
    """

    st.session_state.logged_in = True
    st.session_state.user = user
    st.session_state.user_id = user.id
    st.session_state.user_name = user.full_name
    st.session_state.user_email = user.email


def logout_session():
    """
    Clear the user session.
    """

    keys = [
        "logged_in",
        "user",
        "user_id",
        "user_name",
        "user_email",
    ]

    for key in keys:
        st.session_state.pop(key, None)


def is_logged_in() -> bool:
    """
    Check whether the user is logged in.
    """

    return st.session_state.get("logged_in", False)