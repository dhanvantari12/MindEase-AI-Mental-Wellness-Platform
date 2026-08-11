"""
Insights page for MindEase.

Provides simple personalized wellness insights
based on mood and journal activity.
"""

import streamlit as st

from ui.navigation import navigate
from utils.session import is_logged_in

from features.mood.services import (
    get_user_moods,
    get_weekly_mood_counts,
)

from features.journal.services import (
    get_user_journal_entries,
)


def show_insights_page():
    """Display personalized wellness insights."""

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
    # Load user data
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

    st.title("💡 Your Wellness Insights")

    st.caption(
        "Small observations from your wellness journey."
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
            key="insights_dashboard",
        ):
            navigate("dashboard")

        if st.button(
            "💬 Safe Space",
            use_container_width=True,
            key="insights_safe_space",
        ):
            navigate("safe_space")

        if st.button(
            "😊 Mood Tracker",
            use_container_width=True,
            key="insights_mood",
        ):
            navigate("mood")

        if st.button(
            "📔 Journal",
            use_container_width=True,
            key="insights_journal",
        ):
            navigate("journal")

        if st.button(
            "📊 Statistics",
            use_container_width=True,
            key="insights_statistics",
        ):
            navigate("statistics")

        st.divider()

        if st.button(
            "🔔 Reminders",
            use_container_width=True,
            key="insights_reminders",
        ):
            st.info(
                "Reminders are coming soon."
            )

    # ---------------------------------------------------------
    # No Data State
    # ---------------------------------------------------------

    if not moods and not journal_entries:

        st.info(
            "🌱 Your insights will appear here as "
            "you start using MindEase."
        )

        st.write("")

        st.markdown(
            """
            ### Start your wellness journey

            You can begin by:

            - 😊 Recording your mood
            - 📔 Writing a journal entry
            - 💬 Talking in Safe Space

            The more you use MindEase, the more useful
            your personal insights can become.
            """
        )

        st.write("")

        if st.button(
            "😊 Record Today's Mood",
            use_container_width=True,
            key="insights_start_mood",
        ):
            navigate("mood")

        return

    # ---------------------------------------------------------
    # Mood Analysis
    # ---------------------------------------------------------

    st.subheader("😊 Mood Insights")

    mood_values = [
        mood.mood
        for mood in moods
    ]

    mood_counts = {}

    for mood in mood_values:

        mood_counts[mood] = (
            mood_counts.get(mood, 0) + 1
        )

    # Most common mood
    most_common_mood = max(
        mood_counts,
        key=mood_counts.get,
    )

    most_common_count = mood_counts[
        most_common_mood
    ]

    st.success(
        f"🌸 Your most frequently recorded mood "
        f"is **{most_common_mood}** "
        f"({most_common_count} check-in"
        f"{'s' if most_common_count != 1 else ''})."
    )

    # ---------------------------------------------------------
    # Positive / Negative Mood Analysis
    # ---------------------------------------------------------

    positive_moods = {
        "Great",
        "Good",
    }

    challenging_moods = {
        "Low",
        "Struggling",
    }

    positive_count = sum(
        1
        for mood in mood_values
        if mood in positive_moods
    )

    challenging_count = sum(
        1
        for mood in mood_values
        if mood in challenging_moods
    )

    if positive_count > challenging_count:

        st.info(
            "🌱 You have recorded more positive "
            "moods than challenging moods. "
            "That's a good pattern to notice."
        )

    elif challenging_count > positive_count:

        st.warning(
            "💙 You have recorded more challenging "
            "moods recently. Consider giving yourself "
            "some extra time for rest and reflection."
        )

    else:

        st.info(
            "🌿 Your mood pattern is fairly balanced. "
            "Keep checking in with yourself."
        )

    # ---------------------------------------------------------
    # Weekly Insight
    # ---------------------------------------------------------

    st.write("")

    st.subheader(
        "📅 This Week"
    )

    weekly_total = sum(
        weekly_counts.values()
    )

    if weekly_total == 0:

        st.info(
            "No mood check-ins have been recorded "
            "this week yet."
        )

    else:

        weekly_mood = max(
            weekly_counts,
            key=weekly_counts.get,
        )

        weekly_mood_count = weekly_counts[
            weekly_mood
        ]

        st.info(
            f"📊 You recorded **{weekly_total}** "
            f"mood check-in"
            f"{'s' if weekly_total != 1 else ''} "
            f"this week. Your most common mood was "
            f"**{weekly_mood}**."
        )

        if weekly_mood_count >= 3:

            st.success(
                f"🌱 **{weekly_mood}** appeared "
                f"{weekly_mood_count} times this week."
            )

    # ---------------------------------------------------------
    # Journaling Insight
    # ---------------------------------------------------------

    st.write("")

    st.subheader(
        "📔 Journaling Insight"
    )

    journal_count = len(
        journal_entries
    )

    if journal_count == 0:

        st.info(
            "You haven't written a journal entry yet. "
            "Try writing down what's on your mind."
        )

    elif journal_count == 1:

        st.success(
            "📔 You've written your first journal entry. "
            "Keep using your journal as a private space "
            "for reflection."
        )

    else:

        st.success(
            f"📔 You've written **{journal_count}** "
            f"journal entries. Regular reflection can "
            f"help you notice patterns in your thoughts "
            f"and feelings."
        )

    # ---------------------------------------------------------
    # Wellness Recommendation
    # ---------------------------------------------------------

    st.write("")

    st.subheader(
        "🌱 A Small Suggestion"
    )

    if challenging_count > positive_count:

        st.warning(
            "💙 You've had some challenging mood "
            "check-ins. Consider taking a short break, "
            "writing in your journal, or talking in "
            "Safe Space about what's on your mind."
        )

    elif journal_count == 0:

        st.info(
            "📔 Try writing a short journal entry today. "
            "It doesn't have to be long — even a few "
            "sentences can help you reflect."
        )

    elif weekly_total == 0:

        st.info(
            "😊 Try recording your mood today. "
            "Consistent check-ins help MindEase "
            "understand your wellness patterns."
        )

    else:

        st.success(
            "🌸 You're actively checking in with "
            "yourself. Keep building the habit of "
            "reflection and self-awareness."
        )

    # ---------------------------------------------------------
    # Important Note
    # ---------------------------------------------------------

    st.write("")

    st.caption(
        "💙 These insights are based on your MindEase "
        "activity and are intended for self-reflection, "
        "not medical diagnosis."
    )

    st.write("")

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Dashboard",
            use_container_width=True,
            key="insights_back_dashboard",
        ):
            navigate("dashboard")

    with col2:

        if st.button(
            "📊 View Statistics",
            use_container_width=True,
            key="insights_view_statistics",
        ):
            navigate("statistics")