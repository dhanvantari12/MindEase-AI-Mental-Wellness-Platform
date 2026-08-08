"""
Main dashboard page for MindEase.
"""

import streamlit as st

from ui.components.logout_button import logout_button
from ui.navigation import navigate
from utils.session import is_logged_in
from features.mood.services import get_today_mood


def show_dashboard():
    """Display the main MindEase dashboard."""

    # ---------------------------------------------------------
    # Authentication check
    # ---------------------------------------------------------

    if not is_logged_in():
        st.error("Please login first.")
        return

    # ---------------------------------------------------------
    # Get current user
    # ---------------------------------------------------------

    user_name = st.session_state.get(
        "user_name",
        "there"
    )
    
    user_id = st.session_state.get("user_id")

    today_mood_entry = get_today_mood(user_id)

    if today_mood_entry:
       today_mood = today_mood_entry.mood
    else:
       today_mood = "Not recorded"

    # ---------------------------------------------------------
    # Page Header
    # ---------------------------------------------------------

    st.title("🌸 MindEase Dashboard")

    st.caption(
        "Your personal space for reflection, wellness and growth."
    )

    # ---------------------------------------------------------
    # Sidebar
    # ---------------------------------------------------------

    with st.sidebar:

        st.markdown("## 🌸 MindEase")

        st.caption("Your wellness companion")

        st.divider()

        # Dashboard
        if st.button(
            "🏠 Dashboard",
            use_container_width=True
        ):
            st.rerun()

        # Safe Space
        if st.button(
            "💬 Safe Space",
            use_container_width=True
        ):
            st.info("Safe Space is coming soon.")

        # Mood Tracker
        if st.button(
            "😊 Mood Tracker",
            use_container_width=True
        ):
            navigate("mood")

        # Journal
        if st.button(
            "📔 Journal",
            use_container_width=True
        ):
            st.info("Journal is coming soon.")

        # Reminders
        if st.button(
            "🔔 Reminders",
            use_container_width=True
        ):
            st.info("Reminders are coming soon.")

        # Insights
        if st.button(
            "💡 Insights",
            use_container_width=True
        ):
            st.info("Insights are coming soon.")

        # Statistics
        if st.button(
            "📊 Statistics",
            use_container_width=True
        ):
            st.info("Statistics are coming soon.")

        st.divider()

        # Profile
        if st.button(
            "👤 Profile",
            use_container_width=True
        ):
            st.info("Profile is coming soon.")

        # Settings
        if st.button(
            "⚙️ Settings",
            use_container_width=True
        ):
            st.info("Settings are coming soon.")

        st.divider()

        # Logout
        logout_button()

    # ---------------------------------------------------------
    # Welcome Section
    # ---------------------------------------------------------

    st.success(
        f"👋 Welcome back, {user_name}! 💙"
    )

    st.write("")

    # ---------------------------------------------------------
    # Mood Check-in Section
    # ---------------------------------------------------------

    st.subheader("How are you feeling today?")

    st.caption(
        "Take a moment to check in with yourself."
    )

    # ---------------------------------------------------------
    # Quick Mood Selection
    # ---------------------------------------------------------

    mood_col1, mood_col2, mood_col3, mood_col4, mood_col5 = st.columns(5)

    with mood_col1:
        st.button(
            "😄 Great",
            use_container_width=True
        )

    with mood_col2:
        st.button(
            "🙂 Good",
            use_container_width=True
        )

    with mood_col3:
        st.button(
            "😐 Okay",
            use_container_width=True
        )

    with mood_col4:
        st.button(
            "😔 Low",
            use_container_width=True
        )

    with mood_col5:
        st.button(
            "😞 Struggling",
            use_container_width=True
        )

    st.write("")

    # ---------------------------------------------------------
    # Quick Actions
    # ---------------------------------------------------------

    st.subheader("Quick Actions")

    col1, col2, col3 = st.columns(3)

    # Safe Space
    with col1:

        st.markdown("### 💬")

        st.markdown("#### Safe Space")

        st.caption(
            "Talk freely about what's on your mind."
        )

        if st.button(
            "Start Conversation",
            use_container_width=True
        ):
            st.info(
                "Safe Space is coming soon."
            )

    # Journal
    with col2:

        st.markdown("### 📔")

        st.markdown("#### Journal")

        st.caption(
            "Write down your thoughts and feelings."
        )

        if st.button(
            "Open Journal",
            use_container_width=True
        ):
            st.info(
                "Journal is coming soon."
            )

    # Mood Tracker
    with col3:

        st.markdown("### 😊")

        st.markdown("#### Mood Tracker")

        st.caption(
            "Track how your mood changes over time."
        )

        if st.button(
            "Track Mood",
            use_container_width=True
        ):
            navigate("mood")

    st.write("")

    st.divider()

    # ---------------------------------------------------------
    # Weekly Overview
    # ---------------------------------------------------------

    st.subheader("📊 Your Wellness Overview")

    col1, col2, col3 = st.columns(3)

    # Today's Mood
    with col1:

        st.metric(
           label="😊 Today's Mood",
           value=today_mood
    )

    # Journal Entries
    with col2:

        st.metric(
            label="📔 Journal Entries",
            value="0"
        )

    # Wellness Streak
    with col3:

        st.metric(
            label="🔥 Wellness Streak",
            value="0 days"
        )

    st.write("")

    # ---------------------------------------------------------
    # Recent Activity
    # ---------------------------------------------------------

    st.subheader("🕊️ Recent Activity")

    st.info(
        "Your wellness activity will appear here as you use MindEase."
    )