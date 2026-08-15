"""
Insights page for MindEase.

Displays personalized wellness insights based on
mood and journal activity.
"""

import streamlit as st

from ui.navigation import navigate
from utils.session import is_logged_in

from features.insights.services import (
    get_mood_summary,
    get_weekly_mood_summary,
    get_journal_summary,
    calculate_wellness_score,
    generate_wellness_insights,
)


def show_insights_page():
    """Display the MindEase Insights page."""

    # ---------------------------------------------------------
    # Authentication check
    # ---------------------------------------------------------

    if not is_logged_in():

        st.error("Please login first.")

        return

    # ---------------------------------------------------------
    # Get current user
    # ---------------------------------------------------------

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.error(
            "User session not found. Please login again."
        )

        return

    # ---------------------------------------------------------
    # Load insights data
    # ---------------------------------------------------------

    mood_summary = get_mood_summary(user_id)

    weekly_summary = get_weekly_mood_summary(
        user_id
    )

    journal_summary = get_journal_summary(
        user_id
    )

    wellness_score = calculate_wellness_score(
        user_id
    )

    insights = generate_wellness_insights(
        user_id
    )

    # ---------------------------------------------------------
    # Page Header
    # ---------------------------------------------------------

    st.title("💡 Wellness Insights")

    st.caption(
        "Understand your wellness habits through "
        "your mood and journaling activity."
    )

    st.write("")

    # ---------------------------------------------------------
    # Wellness Score
    # ---------------------------------------------------------

    st.subheader("🌸 Your Wellness Score")

    score_col1, score_col2, score_col3 = st.columns(3)

    with score_col1:

        st.metric(
            label="Wellness Score",
            value=f"{wellness_score}/100",
        )

    with score_col2:

        st.metric(
            label="Mood Check-ins",
            value=mood_summary[
                "total_checkins"
            ],
        )

    with score_col3:

        st.metric(
            label="Journal Entries",
            value=journal_summary[
                "total_entries"
            ],
        )

    st.write("")

    # ---------------------------------------------------------
    # Overall Progress Message
    # ---------------------------------------------------------

    if wellness_score >= 80:

        st.success(
            "🌟 Great job! You're actively engaging "
            "with your wellness journey."
        )

    elif wellness_score >= 50:

        st.info(
            "🌱 You're making progress. Keep building "
            "your wellness habits."
        )

    elif wellness_score > 0:

        st.warning(
            "💙 You're getting started. Small, "
            "consistent steps can make a difference."
        )

    else:

        st.info(
            "🌱 Start recording your mood or writing "
            "journal entries to build your wellness history."
        )

    st.divider()

    # ---------------------------------------------------------
    # Mood Insights
    # ---------------------------------------------------------

    st.subheader("😊 Mood Insights")

    mood_col1, mood_col2, mood_col3 = st.columns(3)

    with mood_col1:

        st.metric(
            label="Total Check-ins",
            value=mood_summary[
                "total_checkins"
            ],
        )

    with mood_col2:

        st.metric(
            label="Most Common Mood",
            value=(
                mood_summary[
                    "most_common_mood"
                ]
                or "None"
            ),
        )

    with mood_col3:

        st.metric(
            label="Latest Mood",
            value=(
                mood_summary[
                    "latest_mood"
                ]
                or "None"
            ),
        )

    # ---------------------------------------------------------
    # Mood Distribution
    # ---------------------------------------------------------

    mood_counts = mood_summary.get(
        "mood_counts",
        {},
    )

    if mood_counts:

        st.write("### 📊 Mood Distribution")

        for mood, count in mood_counts.items():

            st.write(
                f"**{mood}** — {count} check-in"
                f"{'s' if count != 1 else ''}"
            )

            st.progress(
                min(
                    count
                    / max(mood_counts.values()),
                    1.0,
                )
            )

    else:

        st.info(
            "No mood check-ins available yet."
        )

    st.divider()

    # ---------------------------------------------------------
    # Weekly Mood Summary
    # ---------------------------------------------------------

    st.subheader("📅 This Week")

    weekly_col1, weekly_col2 = st.columns(2)

    with weekly_col1:

        st.metric(
            label="This Week's Check-ins",
            value=weekly_summary[
                "total_checkins"
            ],
        )

    with weekly_col2:

        st.metric(
            label="Most Common Mood",
            value=(
                weekly_summary[
                    "most_common_mood"
                ]
                or "None"
            ),
        )

    weekly_moods = weekly_summary.get(
        "mood_counts",
        {},
    )

    if weekly_moods:

        st.write("### Weekly Mood Activity")

        for mood, count in weekly_moods.items():

            st.write(
                f"**{mood}:** {count}"
            )

    else:

        st.info(
            "No mood activity recorded this week."
        )

    st.divider()

    # ---------------------------------------------------------
    # Journal Insights
    # ---------------------------------------------------------

    st.subheader("📔 Journal Insights")

    st.metric(
        label="Total Journal Entries",
        value=journal_summary[
            "total_entries"
        ],
    )

    latest_entry = journal_summary.get(
        "latest_entry"
    )

    if latest_entry:

        # Your service currently returns the
        # complete Journal object.

        entry_title = getattr(
            latest_entry,
            "title",
            "Untitled entry",
        )

        st.info(
            f"📔 Latest journal entry: "
            f"**{entry_title}**"
        )

    else:

        st.info(
            "No journal entries yet. "
            "Start writing to reflect on your day."
        )

    st.divider()

    # ---------------------------------------------------------
    # Personalized Insights
    # ---------------------------------------------------------

    st.subheader(
        "✨ Personalized Insights"
    )

    if insights:

        for insight in insights:

            st.info(insight)

    else:

        st.info(
            "🌱 Keep using MindEase to receive "
            "personalized wellness insights."
        )

    st.divider()

    # ---------------------------------------------------------
    # Quick Actions
    # ---------------------------------------------------------

    st.subheader(
        "🌱 Continue Your Wellness Journey"
    )

    action_col1, action_col2, action_col3 = (
        st.columns(3)
    )

    with action_col1:

        if st.button(
            "😊 Record Mood",
            use_container_width=True,
            key="insights_record_mood",
        ):

            navigate("mood")

    with action_col2:

        if st.button(
            "📔 Open Journal",
            use_container_width=True,
            key="insights_open_journal",
        ):

            navigate("journal")

    with action_col3:

        if st.button(
            "💬 Safe Space",
            use_container_width=True,
            key="insights_open_safe_space",
        ):

            navigate("safe_space")

    st.write("")

    # ---------------------------------------------------------
    # Disclaimer
    # ---------------------------------------------------------

    st.caption(
        "💙 MindEase insights are intended for "
        "self-reflection and wellness engagement. "
        "They are not a medical diagnosis."
    )

    # ---------------------------------------------------------
    # Sidebar Navigation
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
            key="insights_sidebar_dashboard",
        ):

            navigate("dashboard")

        if st.button(
            "💬 Safe Space",
            use_container_width=True,
            key="insights_sidebar_safe_space",
        ):

            navigate("safe_space")

        if st.button(
            "😊 Mood Tracker",
            use_container_width=True,
            key="insights_sidebar_mood",
        ):

            navigate("mood")

        if st.button(
            "📔 Journal",
            use_container_width=True,
            key="insights_sidebar_journal",
        ):

            navigate("journal")

        if st.button(
            "🔔 Reminders",
            use_container_width=True,
            key="insights_sidebar_reminders",
        ):

            navigate("reminders")

        if st.button(
            "💡 Insights",
            use_container_width=True,
            key="insights_sidebar_insights",
        ):

            st.rerun()

        if st.button(
            "📊 Statistics",
            use_container_width=True,
            key="insights_sidebar_statistics",
        ):

            navigate("statistics")

        st.divider()

        if st.button(
            "👤 Profile",
            use_container_width=True,
            key="insights_sidebar_profile",
        ):

            st.info(
                "Profile is coming soon."
            )

        if st.button(
            "⚙️ Settings",
            use_container_width=True,
            key="insights_sidebar_settings",
        ):

            st.info(
                "Settings are coming soon."
            )