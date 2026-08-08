"""
Mood Tracker page for MindEase.
"""

import streamlit as st

from features.mood.services import (
    create_mood,
    get_user_moods,
    get_weekly_mood_counts,
)
from ui.navigation import navigate
from utils.session import is_logged_in


def show_mood_page():
    """Display the MindEase mood tracker page."""

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

    # ---------------------------------------------------------
    # Page Header
    # ---------------------------------------------------------

    st.title("😊 Mood Tracker")

    st.caption(
        "Take a moment to check in with yourself."
    )

    st.write("")

    # ---------------------------------------------------------
    # Mood Check-in
    # ---------------------------------------------------------

    st.subheader("How are you feeling right now?")

    st.caption(
        "There is no right or wrong answer. "
        "Just choose what feels closest to how you feel."
    )

    mood_options = {
        "😄 Great": "Great",
        "🙂 Good": "Good",
        "😐 Okay": "Okay",
        "😔 Low": "Low",
        "😞 Struggling": "Struggling",
    }

    selected_mood = st.radio(
        "Select your mood",
        options=list(mood_options.keys()),
        horizontal=True,
    )

    mood_value = mood_options[selected_mood]

    # ---------------------------------------------------------
    # Mood Note
    # ---------------------------------------------------------

    note = st.text_area(
        "What's on your mind?",
        placeholder=(
            "You can write a few words about how you're feeling..."
        ),
        height=120,
    )

    st.write("")

    # ---------------------------------------------------------
    # Save Mood
    # ---------------------------------------------------------

    if st.button(
        "💾 Save Mood Check-in",
        use_container_width=True,
    ):
        mood_entry = create_mood(
            user_id=user_id,
            mood=mood_value,
            note=note,
        )

        st.success(
            f"Your mood '{mood_entry.mood}' has been recorded. 💙"
        )

        st.rerun()

    # ---------------------------------------------------------
    # Mood History
    # ---------------------------------------------------------

    st.divider()

    st.subheader("📖 Your Mood History")

    moods = get_user_moods(user_id)

    if not moods:

        st.info(
            "You haven't recorded any moods yet. "
            "Your check-ins will appear here."
        )

    else:

        for mood_entry in moods:

            mood_emoji = {
                "Great": "😄",
                "Good": "🙂",
                "Okay": "😐",
                "Low": "😔",
                "Struggling": "😞",
            }.get(
                mood_entry.mood,
                "😊",
            )

            st.markdown(
                f"### {mood_emoji} {mood_entry.mood}"
            )

            if mood_entry.note:
                st.write(mood_entry.note)

            st.caption(
                mood_entry.created_at.strftime(
                    "%d %B %Y, %I:%M %p"
                )
            )

            st.divider()

    # ---------------------------------------------------------
    # Weekly Mood Summary
    # ---------------------------------------------------------

    st.subheader("📊 Your Mood This Week")

    st.caption(
        "A quick look at how you've been feeling this week."
    )

    weekly_counts = get_weekly_mood_counts(user_id)

    mood_col1, mood_col2, mood_col3, mood_col4, mood_col5 = (
        st.columns(5)
    )

    with mood_col1:
        st.metric(
            label="😄 Great",
            value=weekly_counts.get("Great", 0),
        )

    with mood_col2:
        st.metric(
            label="🙂 Good",
            value=weekly_counts.get("Good", 0),
        )

    with mood_col3:
        st.metric(
            label="😐 Okay",
            value=weekly_counts.get("Okay", 0),
        )

    with mood_col4:
        st.metric(
            label="😔 Low",
            value=weekly_counts.get("Low", 0),
        )

    with mood_col5:
        st.metric(
            label="😞 Struggling",
            value=weekly_counts.get("Struggling", 0),
        )

    # ---------------------------------------------------------
    # Weekly Reflection
    # ---------------------------------------------------------

    total_checkins = sum(weekly_counts.values())

    st.write("")

    if total_checkins > 0:

        most_frequent_mood = max(
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

        mood_emoji = mood_emojis.get(
            most_frequent_mood,
            "😊",
        )

        st.info(
            f"🌱 **Weekly Reflection**\n\n"
            f"Your most frequent mood this week was "
            f"**{mood_emoji} {most_frequent_mood}**.\n\n"
            f"You've recorded **{total_checkins} mood "
            f"check-ins** this week."
        )

    else:

        st.info(
            "🌱 **Weekly Reflection**\n\n"
            "You haven't recorded any moods this week yet. "
            "Check in with yourself to start building your "
            "wellness history."
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