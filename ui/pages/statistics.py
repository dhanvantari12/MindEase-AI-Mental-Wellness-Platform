"""
Statistics page for MindEase.

Displays wellness statistics based on
mood check-ins and journal activity.
"""

import streamlit as st

from features.statistics.services import (
    get_wellness_summary,
    get_weekly_mood_counts,
)

from ui.navigation import navigate
from ui.components.logout_button import logout_button
from utils.session import is_logged_in


def show_statistics_page():
    """Display the MindEase statistics page."""

    # ---------------------------------------------------------
    # Authentication check
    # ---------------------------------------------------------

    if not is_logged_in():
        st.error("Please login first.")
        return

    # ---------------------------------------------------------
    # Current user
    # ---------------------------------------------------------

    user_id = st.session_state.get(
        "user_id"
    )

    # ---------------------------------------------------------
    # Get statistics
    # ---------------------------------------------------------

    summary = get_wellness_summary(
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
        "Understand your wellness journey through "
        "your mood and journal activity."
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

        # Dashboard
        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
        ):
            navigate("dashboard")

        # Safe Space
        if st.button(
            "💬 Safe Space",
            use_container_width=True,
        ):
            navigate("safe_space")

        # Mood Tracker
        if st.button(
            "😊 Mood Tracker",
            use_container_width=True,
        ):
            navigate("mood")

        # Journal
        if st.button(
            "📔 Journal",
            use_container_width=True,
        ):
            navigate("journal")

        # Statistics
        if st.button(
            "📊 Statistics",
            use_container_width=True,
        ):
            st.rerun()

        st.divider()

        # Future features
        if st.button(
            "🔔 Reminders",
            use_container_width=True,
        ):
            st.info(
                "Reminders are coming soon."
            )

        if st.button(
            "💡 Insights",
            use_container_width=True,
        ):
            st.info(
                "Insights are coming soon."
            )

        st.divider()

        # Logout
        logout_button()

    # ---------------------------------------------------------
    # Overview Metrics
    # ---------------------------------------------------------

    st.subheader(
        "🌱 Your Wellness Overview"
    )

    col1, col2, col3 = st.columns(3)

    # Total mood check-ins
    with col1:

        st.metric(
            label="😊 Mood Check-ins",
            value=summary[
                "total_mood_checkins"
            ],
        )

    # Journal entries
    with col2:

        st.metric(
            label="📔 Journal Entries",
            value=summary[
                "total_journal_entries"
            ],
        )

    # Most frequent mood
    with col3:

        most_frequent_mood = (
            summary[
                "most_frequent_mood"
            ]
        )

        if most_frequent_mood:

            mood_emojis = {
                "Great": "😄",
                "Good": "🙂",
                "Okay": "😐",
                "Low": "😔",
                "Struggling": "😞",
            }

            mood_display = (
                mood_emojis.get(
                    most_frequent_mood,
                    "😊",
                )
                + " "
                + most_frequent_mood
            )

        else:

            mood_display = "No data"

        st.metric(
            label="💭 Most Frequent Mood",
            value=mood_display,
        )

    st.write("")

    st.divider()

    # ---------------------------------------------------------
    # Mood Distribution
    # ---------------------------------------------------------

    st.subheader(
        "😊 Mood Distribution"
    )

    st.caption(
        "A breakdown of the moods you've recorded."
    )

    mood_distribution = summary[
        "mood_distribution"
    ]

    if sum(
        mood_distribution.values()
    ) == 0:

        st.info(
            "No mood data available yet. "
            "Start recording your moods to see "
            "your statistics."
        )

    else:

        mood_labels = list(
            mood_distribution.keys()
        )

        mood_values = list(
            mood_distribution.values()
        )

        chart_data = {
            "Mood": mood_labels,
            "Check-ins": mood_values,
        }

        st.bar_chart(
            chart_data,
            x="Mood",
            y="Check-ins",
        )

    st.write("")

    # ---------------------------------------------------------
    # Weekly Mood Summary
    # ---------------------------------------------------------

    st.subheader(
        "📅 This Week's Mood"
    )

    st.caption(
        "Your mood check-ins from Monday until today."
    )

    weekly_total = sum(
        weekly_counts.values()
    )

    if weekly_total == 0:

        st.info(
            "No mood check-ins recorded this week yet."
        )

    else:

        weekly_chart_data = {
            "Mood": list(
                weekly_counts.keys()
            ),
            "Check-ins": list(
                weekly_counts.values()
            ),
        }

        st.bar_chart(
            weekly_chart_data,
            x="Mood",
            y="Check-ins",
        )

    st.write("")

    # ---------------------------------------------------------
    # Mood Summary
    # ---------------------------------------------------------

    st.divider()

    st.subheader(
        "🌿 Your Wellness Reflection"
    )

    if weekly_total == 0:

        st.info(
            "You haven't recorded a mood this week yet. "
            "Take a moment to check in with yourself."
        )

    else:

        weekly_most_frequent = max(
            weekly_counts,
            key=weekly_counts.get,
        )

        mood_emojis = {
            "Great": "😄",
            "Good": "🙂",
            "Okay": "😐",
            "Low": "😔",
            "Struggling": "😞",
        }

        emoji = mood_emojis.get(
            weekly_most_frequent,
            "😊",
        )

        st.success(
            f"🌱 Your most frequent mood this week "
            f"has been **{emoji} "
            f"{weekly_most_frequent}**.\n\n"
            f"You've recorded **{weekly_total} "
            f"mood check-ins** this week."
        )

    # ---------------------------------------------------------
    # Back to Dashboard
    # ---------------------------------------------------------

    st.write("")

    if st.button(
        "← Back to Dashboard",
        use_container_width=True,
    ):
        navigate("dashboard")