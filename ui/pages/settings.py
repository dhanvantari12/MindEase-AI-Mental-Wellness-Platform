"""
Settings page for MindEase.

Provides user preferences and account settings.
"""

import streamlit as st

from features.preferences.services import (
    get_or_create_preferences,
    update_preferences,
    update_ai_name,
)

from ui.navigation import navigate
from ui.components.logout_button import logout_button
from utils.session import is_logged_in


def show_settings_page():
    """
    Display the MindEase settings page.
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

    user_name = st.session_state.get(
        "user_name",
        "User",
    )

    user_email = st.session_state.get(
        "user_email",
        "",
    )

    user_id = st.session_state.get(
        "user_id",
    )

    if not user_id:

        st.error(
            "User session not found. Please login again."
        )

        return

    # ---------------------------------------------------------
    # Load preferences
    # ---------------------------------------------------------

    preferences = get_or_create_preferences(
        user_id
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

    st.divider()

    # ---------------------------------------------------------
    # AI Companion Section
    # ---------------------------------------------------------

    st.subheader("🤖 AI Companion")

    st.caption(
        "Give your AI wellness companion a name that feels "
        "comfortable and personal."
    )

    current_ai_name = (
        preferences.ai_name
        if preferences.ai_name
        else "MindEase"
    )

    ai_name = st.text_input(
        "AI companion name",
        value=current_ai_name,
        max_chars=50,
        key="settings_ai_name",
        placeholder="e.g. Nova, Mira, Luna...",
    )

    st.caption(
        "This name will be used by your AI companion "
        "inside Safe Space."
    )

    st.divider()

    # ---------------------------------------------------------
    # Wellness Preferences
    # ---------------------------------------------------------

    st.subheader(
        "🌸 Wellness Preferences"
    )

    st.caption(
        "Choose which MindEase features you would like "
        "to use."
    )

    # ---------------------------------------------------------
    # Reminder Preference
    # ---------------------------------------------------------

    reminder_enabled = st.toggle(
        "🔔 Enable wellness reminders",
        value=preferences.reminders_enabled,
        key="settings_reminders_toggle",
    )

    if reminder_enabled:

        st.success(
            "🔔 Wellness reminders are enabled."
        )

    else:

        st.info(
            "🔕 Wellness reminders are disabled."
        )

    st.write("")

    # ---------------------------------------------------------
    # Daily Check-in
    # ---------------------------------------------------------

    daily_checkin = st.toggle(
        "😊 Daily mood check-in",
        value=preferences.daily_checkin_enabled,
        key="settings_daily_checkin_toggle",
    )

    # ---------------------------------------------------------
    # Journal Prompts
    # ---------------------------------------------------------

    journal_prompt = st.toggle(
        "📔 Journal prompts",
        value=preferences.journal_prompts_enabled,
        key="settings_journal_prompt_toggle",
    )

    st.write("")

    # ---------------------------------------------------------
    # Save Preferences
    # ---------------------------------------------------------

    if st.button(
        "💾 Save Preferences",
        use_container_width=True,
        key="settings_save_preferences",
    ):

        # -----------------------------------------------------
        # Save wellness preferences
        # -----------------------------------------------------

        update_preferences(
            user_id=user_id,
            reminders_enabled=reminder_enabled,
            daily_checkin_enabled=daily_checkin,
            journal_prompts_enabled=journal_prompt,
        )

        # -----------------------------------------------------
        # Save AI companion name
        # -----------------------------------------------------

        update_ai_name(
            user_id=user_id,
            ai_name=ai_name,
        )

        st.success(
            "✅ Your preferences have been saved successfully!"
        )

        st.rerun()

    st.divider()

    # ---------------------------------------------------------
    # Sidebar Navigation
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
            key="settings_sidebar_dashboard",
        ):

            navigate("dashboard")

        # -----------------------------------------------------
        # Safe Space
        # -----------------------------------------------------

        if st.button(
            "💬 Safe Space",
            use_container_width=True,
            key="settings_sidebar_safe_space",
        ):

            navigate("safe_space")

        # -----------------------------------------------------
        # Mood Tracker
        # -----------------------------------------------------

        if st.button(
            "😊 Mood Tracker",
            use_container_width=True,
            key="settings_sidebar_mood",
        ):

            navigate("mood")

        # -----------------------------------------------------
        # Journal
        # -----------------------------------------------------

        if st.button(
            "📔 Journal",
            use_container_width=True,
            key="settings_sidebar_journal",
        ):

            navigate("journal")

        # -----------------------------------------------------
        # Reminders
        # -----------------------------------------------------

        if st.button(
            "🔔 Reminders",
            use_container_width=True,
            key="settings_sidebar_reminders",
        ):

            navigate("reminders")

        # -----------------------------------------------------
        # Insights
        # -----------------------------------------------------

        if st.button(
            "💡 Insights",
            use_container_width=True,
            key="settings_sidebar_insights",
        ):

            navigate("insights")

        # -----------------------------------------------------
        # Statistics
        # -----------------------------------------------------

        if st.button(
            "📊 Statistics",
            use_container_width=True,
            key="settings_sidebar_statistics",
        ):

            navigate("statistics")

        st.divider()

        # -----------------------------------------------------
        # Profile
        # -----------------------------------------------------

        if st.button(
            "👤 Profile",
            use_container_width=True,
            key="settings_sidebar_profile",
        ):

            navigate("profile")

        # -----------------------------------------------------
        # Settings
        # -----------------------------------------------------

        if st.button(
            "⚙️ Settings",
            use_container_width=True,
            key="settings_sidebar_settings",
        ):

            st.rerun()

        st.divider()

        # -----------------------------------------------------
        # Logout
        # -----------------------------------------------------

        logout_button()

    # ---------------------------------------------------------
    # Footer
    # ---------------------------------------------------------

    st.write("")

    st.caption(
        "💙 MindEase is designed for personal wellness "
        "and self-reflection."
    )