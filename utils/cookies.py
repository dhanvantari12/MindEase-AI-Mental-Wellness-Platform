"""
Browser cookie utilities for MindEase.
"""

import streamlit as st
from streamlit_cookies_controller import CookieController


COOKIE_NAME = "mindease_session"

COOKIE_MAX_AGE = 7 * 24 * 60 * 60


def get_cookie_controller():
    """
    Return the Streamlit cookie controller.
    """

    if "cookie_controller" not in st.session_state:
        st.session_state.cookie_controller = CookieController(
            key="mindease_cookie_controller"
        )

    return st.session_state.cookie_controller


def set_session_cookie(token: str) -> None:
    """
    Store the persistent session token
    in the browser cookie.
    """

    controller = get_cookie_controller()

    controller.set(
        COOKIE_NAME,
        token,
        max_age=COOKIE_MAX_AGE,
    )


def get_session_cookie() -> str | None:
    """
    Retrieve the persistent session token
    from the browser cookie.
    """

    controller = get_cookie_controller()

    token = controller.get(COOKIE_NAME)

    if token is None:
        return None

    return str(token)


def delete_session_cookie() -> None:
    """
    Remove the persistent session cookie.
    """

    controller = get_cookie_controller()

    controller.remove(COOKIE_NAME)