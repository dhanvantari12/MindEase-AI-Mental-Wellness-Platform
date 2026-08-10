"""
Session management utilities for MindEase.
"""

import streamlit as st

from features.auth.session_service import (
    create_session,
    delete_session,
    get_user_from_session,
)

from utils.cookies import (
    delete_session_cookie,
    get_session_cookie,
    set_session_cookie,
)


def login_session(user):
    """
    Store logged-in user information
    and create a persistent browser session.
    """

    # ---------------------------------------------------------
    # Streamlit session
    # ---------------------------------------------------------

    st.session_state.logged_in = True
    st.session_state.user = user
    st.session_state.user_id = str(user.id)
    st.session_state.user_name = user.full_name
    st.session_state.user_email = user.email

    # ---------------------------------------------------------
    # Persistent session
    # ---------------------------------------------------------

    token = create_session(
        user_id=user.id
    )

    set_session_cookie(token)


def restore_session() -> bool:
    """
    Restore the logged-in user from the
    persistent browser session.

    Returns:
        True if a valid session was restored.
        False otherwise.
    """

    # ---------------------------------------------------------
    # Already logged in
    # ---------------------------------------------------------

    if st.session_state.get(
        "logged_in",
        False,
    ):
        return True

    # ---------------------------------------------------------
    # Get browser cookie
    # ---------------------------------------------------------

    token = get_session_cookie()

    if not token:

        return False

    # ---------------------------------------------------------
    # Validate token
    # ---------------------------------------------------------

    user = get_user_from_session(
        token
    )

    if user is None:

        delete_session_cookie()

        return False

    # ---------------------------------------------------------
    # Restore user
    # ---------------------------------------------------------

    st.session_state.logged_in = True
    st.session_state.user = user
    st.session_state.user_id = str(user.id)
    st.session_state.user_name = user.full_name
    st.session_state.user_email = user.email

    return True


def logout_session():
    """
    Clear the Streamlit session and
    persistent browser session.
    """

    # ---------------------------------------------------------
    # Get current persistent token
    # ---------------------------------------------------------

    token = get_session_cookie()

    # ---------------------------------------------------------
    # Delete database session
    # ---------------------------------------------------------

    if token:

        delete_session(
            token
        )

    # ---------------------------------------------------------
    # Delete browser cookie
    # ---------------------------------------------------------

    delete_session_cookie()

    # ---------------------------------------------------------
    # Clear Streamlit session
    # ---------------------------------------------------------

    keys = [
        "logged_in",
        "user",
        "user_id",
        "user_name",
        "user_email",
        "user",
    ]

    for key in keys:

        st.session_state.pop(
            key,
            None,
        )

    # ---------------------------------------------------------
    # Reset login state
    # ---------------------------------------------------------

    st.session_state.logged_in = False
    st.session_state.user_id = None


def is_logged_in() -> bool:
    """
    Check whether the user is logged in.
    """

    return st.session_state.get(
        "logged_in",
        False,
    )