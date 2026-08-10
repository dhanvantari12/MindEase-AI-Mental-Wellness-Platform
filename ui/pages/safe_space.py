"""
Safe Space page for MindEase.

Provides a supportive AI conversation interface
with persistent conversation history.
"""

import streamlit as st

from features.safe_space.services import (
    generate_response,
    save_message,
    get_conversation,
    clear_conversation,
)

from ui.navigation import navigate
from utils.session import is_logged_in


def show_safe_space_page():
    """
    Display the MindEase Safe Space.
    """

    # ---------------------------------------------------------
    # Authentication check
    # ---------------------------------------------------------

    if not is_logged_in():
        st.error("Please login first.")
        return

    # ---------------------------------------------------------
    # Current user
    # ---------------------------------------------------------

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("User session not found. Please login again.")
        return

    # ---------------------------------------------------------
    # Page Header
    # ---------------------------------------------------------

    st.title("💬 Safe Space")

    st.caption(
        "A calm space where you can talk, reflect, and be heard."
    )

    st.write("")

    # ---------------------------------------------------------
    # Load conversation history
    # ---------------------------------------------------------

    messages = get_conversation(user_id)

    # ---------------------------------------------------------
    # Welcome message
    # ---------------------------------------------------------

    if not messages:

        st.info(
            "🌸 Welcome to Safe Space.\n\n"
            "You can talk about what's on your mind. "
            "I'm here to listen without judgment."
        )

    # ---------------------------------------------------------
    # Display conversation history
    # ---------------------------------------------------------

    for message in messages:

        with st.chat_message(message.role):

            st.markdown(message.content)

    # ---------------------------------------------------------
    # Chat input
    # ---------------------------------------------------------

    user_message = st.chat_input(
        "What's on your mind?"
    )

    if user_message:

        # -----------------------------------------------------
        # Save user message
        # -----------------------------------------------------

        save_message(
            user_id=user_id,
            role="user",
            content=user_message,
        )

        # -----------------------------------------------------
        # Display user message
        # -----------------------------------------------------

        with st.chat_message("user"):

            st.markdown(user_message)

        # -----------------------------------------------------
        # Generate AI response
        # -----------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "MindEase is thinking..."
            ):

                try:

                    response = generate_response(
                        user_message
                    )

                except Exception as error:

                    response = (
                        "I'm sorry, I couldn't process that "
                        "right now. Please try again in a moment."
                    )

                    st.error(
                        f"Safe Space error: {error}"
                    )

            st.markdown(response)

        # -----------------------------------------------------
        # Save AI response
        # -----------------------------------------------------

        save_message(
            user_id=user_id,
            role="assistant",
            content=response,
        )

    # ---------------------------------------------------------
    # Sidebar
    # ---------------------------------------------------------

    with st.sidebar:

        st.markdown("## 🌸 MindEase")

        st.caption(
            "Your wellness companion"
        )

        st.divider()

        # -----------------------------------------------------
        # Dashboard
        # -----------------------------------------------------

        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
        ):

            navigate("dashboard")

        # -----------------------------------------------------
        # Safe Space
        # -----------------------------------------------------

        if st.button(
            "💬 Safe Space",
            use_container_width=True,
        ):

            navigate("safe_space")

        # -----------------------------------------------------
        # Mood Tracker
        # -----------------------------------------------------

        if st.button(
            "😊 Mood Tracker",
            use_container_width=True,
        ):

            navigate("mood")

        # -----------------------------------------------------
        # Journal
        # -----------------------------------------------------

        if st.button(
            "📔 Journal",
            use_container_width=True,
        ):

            navigate("journal")

        st.divider()

        # -----------------------------------------------------
        # Clear Conversation
        # -----------------------------------------------------

        if st.button(
            "🗑️ Clear Conversation",
            use_container_width=True,
        ):

            clear_conversation(user_id)

            st.success(
                "Conversation cleared."
            )

            st.rerun()

        st.divider()

        # -----------------------------------------------------
        # Back to Dashboard
        # -----------------------------------------------------

        if st.button(
            "← Back to Dashboard",
            use_container_width=True,
        ):

            navigate("dashboard")