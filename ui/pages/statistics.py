"""
Statistics page for MindEase.

Displays personal wellness statistics based on
mood check-ins and journal activity.
"""

import streamlit as st
import pandas as pd

from ui.navigation import navigate
from utils.session import is_logged_in

from features.mood.services import (
    get_user_moods,
    get_weekly_mood_counts,
)

from features.journal.services import (
    get_user_journal_entries,
)


def show_statistics_page():
    """Display the MindEase Statistics page."""

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
        st.error(
            "User session not found. Please login again."
        )
        return

    # ---------------------------------------------------------
    # Load data
    # ---------------------------------------------------------

    moods = get_user_moods(user_id)

    journal_entries = get_user_journal_entries(
        user_id
    )

    weekly_counts = get_weekly_mood_counts(
        user_id
    )

    # ---------------------------------------------------------
    # Page Header
    # ---------------------------------------------------------

    st.title("📊 Wellness Statistics")

    st.caption(
        "Understand your wellness patterns through "
        "your mood and journaling activity."
    )

    st.write("")

    # ---------------------------------------------------------
    # Sidebar
    # ---------------------------------------------------------

    with st.sidebar:

        st.markdown("## 🌸 MindEase")

        st.caption(
            "Your wellness companion"
        )

        st.divider()

        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
            key="statistics_dashboard",
        ):
            navigate("dashboard")

        if st.button(
            "💬 Safe Space",
            use_container_width=True,
            key="statistics_safe_space",
        ):
            navigate("safe_space")

        if st.button(
            "😊 Mood Tracker",
            use_container_width=True,
            key="statistics_mood",
        ):
            navigate("mood")

        if st.button(
            "📔 Journal",
            use_container_width=True,
            key="statistics_journal",
        ):
            navigate("journal")

        st.divider()

        if st.button(
            "💡 Insights",
            use_container_width=True,
            key="statistics_insights",
        ):
            st.info(
                "Insights are coming soon."
            )

        if st.button(
            "⚙️ Settings",
            use_container_width=True,
            key="statistics_settings",
        ):
            st.info(
                "Settings are coming soon."
            )

    # ---------------------------------------------------------
    # Summary Cards
    # ---------------------------------------------------------

    st.subheader("📌 Your Wellness Summary")

    col1, col2, col3 = st.columns(3)

    # Total mood check-ins
    with col1:

        st.metric(
            "😊 Total Mood Check-ins",
            len(moods),
        )

    # Total journal entries
    with col2:

        st.metric(
            "📔 Journal Entries",
            len(journal_entries),
        )

    # Most common mood
    with col3:

        if moods:

            mood_values = [
                mood.mood
                for mood in moods
            ]

            most_common_mood = max(
                set(mood_values),
                key=mood_values.count,
            )

        else:

            most_common_mood = "Not recorded"

        st.metric(
            "🌸 Most Common Mood",
            most_common_mood,
        )

    st.write("")

    st.divider()

    # ---------------------------------------------------------
    # Weekly Mood Distribution
    # ---------------------------------------------------------

    st.subheader(
        "📅 This Week's Mood Distribution"
    )

    total_weekly_moods = sum(
        weekly_counts.values()
    )

    if total_weekly_moods == 0:

        st.info(
            "No mood check-ins recorded this week yet."
        )

    else:

        weekly_df = pd.DataFrame(
            {
                "Mood": list(
                    weekly_counts.keys()
                ),
                "Check-ins": list(
                    weekly_counts.values()
                ),
            }
        )

        st.bar_chart(
            weekly_df.set_index("Mood")
        )

    st.write("")

    # ---------------------------------------------------------
    # Overall Mood Distribution
    # ---------------------------------------------------------

    st.subheader(
        "😊 Overall Mood Distribution"
    )

    if not moods:

        st.info(
            "Start recording your moods to see "
            "your overall mood distribution."
        )

    else:

        mood_counts = {}

        for mood in moods:

            mood_counts[mood.mood] = (
                mood_counts.get(
                    mood.mood,
                    0,
                )
                + 1
            )

        mood_df = pd.DataFrame(
            {
                "Mood": list(
                    mood_counts.keys()
                ),
                "Check-ins": list(
                    mood_counts.values()
                ),
            }
        )

        st.bar_chart(
            mood_df.set_index("Mood")
        )

    st.write("")

    # ---------------------------------------------------------
    # Journal Activity
    # ---------------------------------------------------------

    st.subheader(
        "📔 Journal Activity"
    )

    if not journal_entries:

        st.info(
            "You haven't written any journal entries yet."
        )

    else:

        st.success(
            f"You have written "
            f"**{len(journal_entries)}** "
            f"journal entr"
            f"{'y' if len(journal_entries) == 1 else 'ies'}."
        )

        st.caption(
            "Writing regularly can help you reflect "
            "on your thoughts and emotions."
        )

    st.write("")

    # ---------------------------------------------------------
    # Wellness Summary
    # ---------------------------------------------------------

    st.divider()

    st.subheader(
        "🕊️ Your Wellness Summary"
    )

    if not moods and not journal_entries:

        st.info(
            "Your wellness journey is just beginning. "
            "Record a mood or write a journal entry "
            "to start building your personal insights."
        )

    else:

        if total_weekly_moods > 0:

            st.success(
                f"🌱 You recorded "
                f"**{total_weekly_moods}** "
                f"mood check-in"
                f"{'s' if total_weekly_moods != 1 else ''} "
                f"this week."
            )

        if journal_entries:

            st.info(
                f"📔 You have "
                f"**{len(journal_entries)}** "
                f"journal entr"
                f"{'ies' if len(journal_entries) != 1 else 'y'} "
                f"to reflect on."
            )

    st.write("")

    # ---------------------------------------------------------
    # Back to Dashboard
    # ---------------------------------------------------------

    if st.button(
        "← Back to Dashboard",
        use_container_width=True,
        key="statistics_back_dashboard",
    ):

        navigate("dashboard")