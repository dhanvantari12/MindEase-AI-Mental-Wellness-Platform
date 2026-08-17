"""
Safe Space page for MindEase.

Provides a supportive AI conversation interface
with persistent conversation history,
personalized AI companion name, and
long-term user memory.
"""

import streamlit as st

from features.safe_space.services import (
    generate_response,
    save_message,
    get_conversation,
    clear_conversation,
)

from features.preferences.services import get_ai_name

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

        st.error(
            "Please login first."
        )

        return

    # ---------------------------------------------------------
    # Current user
    # ---------------------------------------------------------

    user_id = st.session_state.get(
        "user_id"
    )

    if not user_id:

        st.error(
            "User session not found. Please login again."
        )

        return

    # ---------------------------------------------------------
    # Get personalized AI companion name
    # ---------------------------------------------------------

    ai_name = (
        get_ai_name(user_id)
        or "MindEase"
    )

    # ---------------------------------------------------------
    # Page Header
    # ---------------------------------------------------------

    st.title(
        f"💬 Safe Space with {ai_name}"
    )

    st.caption(
        f"A calm space where you can talk, reflect, "
        f"and be heard by {ai_name}."
    )

    st.write("")

    # ---------------------------------------------------------
    # Load conversation history
    # ---------------------------------------------------------

    messages = get_conversation(
        user_id
    )

    # ---------------------------------------------------------
    # Welcome message
    # ---------------------------------------------------------

    if not messages:

        st.info(
            f"🌸 Welcome to Safe Space.\n\n"
            f"I'm {ai_name}, your personal wellness "
            "companion. I'm here to listen without "
            "judgment."
        )

    # ---------------------------------------------------------
    # Display conversation history
    # ---------------------------------------------------------

    for message in messages:

        with st.chat_message(
            message.role
        ):

            st.markdown(
                message.content
            )

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

            st.markdown(
                user_message
            )

        # -----------------------------------------------------
        # Generate AI response
        # -----------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                f"{ai_name} is thinking..."
            ):

                try:

                    response = generate_response(
                        user_message=user_message,
                        user_id=user_id,
                        ai_name=ai_name,
                    )

                except Exception as error:

                    response = (
                        "I'm sorry, I couldn't process "
                        "that right now. Please try again "
                        "in a moment."
                    )

                    st.error(
                        f"Safe Space error: {error}"
                    )

            st.markdown(
                response
            )

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

        st.markdown(
            "## 🌸 MindEase"
        )

        st.caption(
            f"Your wellness companion: {ai_name}"
        )

        st.divider()

        # -----------------------------------------------------
        # Dashboard
        # -----------------------------------------------------

        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
            key="safe_space_sidebar_dashboard",
        ):

            navigate(
                "dashboard"
            )

        # -----------------------------------------------------
        # Safe Space
        # -----------------------------------------------------

        if st.button(
            "💬 Safe Space",
            use_container_width=True,
            key="safe_space_sidebar_safe_space",
        ):

            navigate(
                "safe_space"
            )

        # -----------------------------------------------------
        # Mood Tracker
        # -----------------------------------------------------

        if st.button(
            "😊 Mood Tracker",
            use_container_width=True,
            key="safe_space_sidebar_mood",
        ):

            navigate(
                "mood"
            )

        # -----------------------------------------------------
        # Journal
        # -----------------------------------------------------

        if st.button(
            "📔 Journal",
            use_container_width=True,
            key="safe_space_sidebar_journal",
        ):

            navigate(
                "journal"
            )

        # -----------------------------------------------------
        # Reminders
        # -----------------------------------------------------

        if st.button(
            "🔔 Reminders",
            use_container_width=True,
            key="safe_space_sidebar_reminders",
        ):

            navigate(
                "reminders"
            )

        # -----------------------------------------------------
        # Insights
        # -----------------------------------------------------

        if st.button(
            "💡 Insights",
            use_container_width=True,
            key="safe_space_sidebar_insights",
        ):

            navigate(
                "insights"
            )

        # -----------------------------------------------------
        # Statistics
        # -----------------------------------------------------

        if st.button(
            "📊 Statistics",
            use_container_width=True,
            key="safe_space_sidebar_statistics",
        ):

            navigate(
                "statistics"
            )

        st.divider()

        # -----------------------------------------------------
        # Profile
        # -----------------------------------------------------

        if st.button(
            "👤 Profile",
            use_container_width=True,
            key="safe_space_sidebar_profile",
        ):

            navigate(
                "profile"
            )

        # -----------------------------------------------------
        # Settings
        # -----------------------------------------------------

        if st.button(
            "⚙️ Settings",
            use_container_width=True,
            key="safe_space_sidebar_settings",
        ):

            navigate(
                "settings"
            )

        st.divider()

        # -----------------------------------------------------
        # Clear Conversation
        # -----------------------------------------------------

        if st.button(
            "🗑️ Clear Conversation",
            use_container_width=True,
            key="safe_space_clear_conversation",
        ):

            clear_conversation(
                user_id
            )

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
            key="safe_space_back_dashboard",
        ):

            navigate(
                "dashboard"
            )

    # ---------------------------------------------------------
    # Footer
    # ---------------------------------------------------------

    st.write("")

    st.caption(
        f"💙 {ai_name} is designed to support personal "
        "wellness and self-reflection."
    )