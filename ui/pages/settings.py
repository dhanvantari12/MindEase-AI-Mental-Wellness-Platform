"""
Settings page for MindEase.

Provides user preferences and account settings.
"""

import streamlit as st

from ui.navigation import navigate
from utils.session import is_logged_in
from ui.components.logout_button import logout_button


def show_settings_page():
    """Display the MindEase settings page."""

    # ---------------------------------------------------------
    # Authentication check
    # ---------------------------------------------------------

    if not is_logged_in():

        st.error("Please login first.")

        return

    # ---------------------------------------------------------
    # Current user
    # ---------------------------------------------------------

    user_name = st.session_state.get(
        "user_name",
        "User",
    )

    user_email = st.session_state.get(
        "user_email",
        "",
    )

    # ---------------------------------------------------------
    # Page Header
    # ---------------------------------------------------------

    st.title("⚙️ Settings")

    st.caption(
        "Customize your MindEase experience."
    )

    st.write("")

    # ---------------------------------------------------------
    # Account Section
    # ---------------------------------------------------------

    st.subheader("👤 Account")

    account_col1, account_col2 = st.columns(2)

    with account_col1:

        st.write("**Name**")

        st.info(
            user_name
        )

    with account_col2:

        st.write("**Email**")

        st.info(
            user_email
        )

    st.write("")

    # ---------------------------------------------------------
    # Reminder Preferences
    # ---------------------------------------------------------

    st.subheader(
        "🔔 Reminder Preferences"
    )

    reminder_enabled = st.toggle(
        "Enable wellness reminders",
        value=st.session_state.get(
            "reminders_enabled",
            True,
        ),
        key="settings_reminders_toggle",
    )

    st.session_state.reminders_enabled = (
        reminder_enabled
    )

    if reminder_enabled:

        st.success(
            "🔔 Wellness reminders are enabled."
        )

    else:

        st.info(
            "🔕 Wellness reminders are disabled."
        )

    st.divider()

    # ---------------------------------------------------------
    # Wellness Preferences
    # ---------------------------------------------------------

    st.subheader(
        "🌸 Wellness Preferences"
    )

    daily_checkin = st.toggle(
        "Daily mood check-in",
        value=st.session_state.get(
            "daily_checkin_enabled",
            True,
        ),
        key="settings_daily_checkin_toggle",
    )

    st.session_state.daily_checkin_enabled = (
        daily_checkin
    )

    journal_prompt = st.toggle(
        "Journal prompts",
        value=st.session_state.get(
            "journal_prompts_enabled",
            True,
        ),
        key="settings_journal_prompt_toggle",
    )

    st.session_state.journal_prompts_enabled = (
        journal_prompt
    )

    st.write("")

    st.caption(
        "These preferences currently apply to this "
        "session. We can persist them in the database "
        "in a later step."
    )

    st.divider()

    # ---------------------------------------------------------
    # Security
    # ---------------------------------------------------------

    st.subheader(
        "🔐 Security"
    )

    st.info(
        "Password management will be added in a "
        "future security update."
    )

    st.write("")

    if st.button(
        "👤 View Profile",
        use_container_width=True,
        key="settings_profile_button",
    ):

        navigate("profile")

    st.divider()

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    with st.sidebar:

        st.markdown(
            "## 🌸 MindEase"
        )

        st.caption(
            "Your wellness companion"
        )

        st.divider()

        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
            key="settings_sidebar_dashboard",
        ):

            navigate("dashboard")

        if st.button(
            "💬 Safe Space",
            use_container_width=True,
            key="settings_sidebar_safe_space",
        ):

            navigate("safe_space")

        if st.button(
            "😊 Mood Tracker",
            use_container_width=True,
            key="settings_sidebar_mood",
        ):

            navigate("mood")

        if st.button(
            "📔 Journal",
            use_container_width=True,
            key="settings_sidebar_journal",
        ):

            navigate("journal")

        if st.button(
            "🔔 Reminders",
            use_container_width=True,
            key="settings_sidebar_reminders",
        ):

            navigate("reminders")

        if st.button(
            "💡 Insights",
            use_container_width=True,
            key="settings_sidebar_insights",
        ):

            navigate("insights")

        if st.button(
            "📊 Statistics",
            use_container_width=True,
            key="settings_sidebar_statistics",
        ):

            navigate("statistics")

        st.divider()

        if st.button(
            "👤 Profile",
            use_container_width=True,
            key="settings_sidebar_profile",
        ):

            navigate("profile")

        if st.button(
            "⚙️ Settings",
            use_container_width=True,
            key="settings_sidebar_settings",
        ):

            st.rerun()

        st.divider()

        logout_button()

    # ---------------------------------------------------------
    # Footer
    # ---------------------------------------------------------

    st.write("")

    st.caption(
        "💙 MindEase is designed for personal wellness "
        "and self-reflection."
    )