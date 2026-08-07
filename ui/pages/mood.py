"""
Mood Tracker page for MindEase.
"""

import streamlit as st

from features.mood.services import (
    create_mood,
    get_user_moods,
)
from ui.navigation import navigate
from utils.session import is_logged_in


MOODS = {
    "😄 Great": "Great",
    "🙂 Good": "Good",
    "😐 Okay": "Okay",
    "😔 Low": "Low",
    "😞 Struggling": "Struggling",
}


def show_mood_page():
    """Display the Mood Tracker page."""

    # ---------------------------------------------------------
    # Authentication check
    # ---------------------------------------------------------

    if not is_logged_in():
        st.error("Please login first.")
        return

    user_id = st.session_state.get("user_id")

    # ---------------------------------------------------------
    # Header
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

    selected_mood = st.radio(
        "Choose your mood",
        options=list(MOODS.keys()),
        horizontal=True,
    )

    st.write("")

    note = st.text_area(
        "What's on your mind?",
        placeholder=(
            "You can write a little about how you're feeling..."
        ),
        height=120,
    )

    st.write("")

    if st.button(
        "Save Mood Check-in",
        use_container_width=True,
    ):

        mood_value = MOODS[selected_mood]

        create_mood(
            user_id=user_id,
            mood=mood_value,
            note=note,
        )

        st.success(
            "🌸 Your mood has been recorded."
        )

        st.balloons()

    # ---------------------------------------------------------
    # Mood History
    # ---------------------------------------------------------

    st.divider()

    st.subheader("📖 Your Mood History")

    moods = get_user_moods(user_id)

    if not moods:

        st.info(
            "You haven't recorded any moods yet."
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

            with st.container():

                col1, col2 = st.columns(
                    [1, 5]
                )

                with col1:
                    st.markdown(
                        f"# {mood_emoji}"
                    )

                with col2:

                    st.markdown(
                        f"**{mood_entry.mood}**"
                    )

                    if mood_entry.note:
                        st.caption(
                            mood_entry.note
                        )

                    st.caption(
                        mood_entry.created_at.strftime(
                            "%d %B %Y, %I:%M %p"
                        )
                    )

                st.divider()

    # ---------------------------------------------------------
    # Back Button
    # ---------------------------------------------------------

    if st.button("← Back to Dashboard"):
        navigate("dashboard")