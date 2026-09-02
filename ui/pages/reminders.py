"""
Daily Wellness Check-In Page.

Morning Mood
Night Reflection
Daily Streak
"""

import streamlit as st

from features.reminders.services import (
    get_today_checkin,
    save_morning_checkin,
    save_night_reflection,
    calculate_streak,
)

from ui.navigation import navigate
from utils.session import is_logged_in


def show_reminders_page():

    if not is_logged_in():
        st.error("Please login first.")
        return

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("User session not found.")
        return

    st.title("🌞 Daily Wellness Check-In")

    streak = calculate_streak(user_id)

    st.success(
        f"🔥 Current Wellness Streak: {streak} day(s)"
    )

    st.divider()

    today_checkin = get_today_checkin(user_id)

    # -------------------------------------------------
    # Morning Mood
    # -------------------------------------------------

    st.subheader("🌅 Morning Check-In")

    current_mood = None

    if today_checkin:
        current_mood = today_checkin.morning_mood

    mood = st.selectbox(
        "How are you feeling this morning?",
        [
            "Great",
            "Good",
            "Okay",
            "Low",
            "Struggling",
        ],
        index=0,
    )

    if st.button(
        "Save Morning Mood",
        use_container_width=True,
    ):

        save_morning_checkin(
            user_id=user_id,
            mood=mood,
        )

        st.success(
            "Morning mood saved!"
        )

        st.rerun()

    if current_mood:

        st.info(
            f"Today's morning mood: {current_mood}"
        )

    st.divider()

    # -------------------------------------------------
    # Night Reflection
    # -------------------------------------------------

    st.subheader("🌙 Night Reflection")

    existing_reflection = ""

    if (
        today_checkin
        and today_checkin.night_reflection
    ):
        existing_reflection = (
            today_checkin.night_reflection
        )

    reflection = st.text_area(
        "How was your day?",
        value=existing_reflection,
        height=150,
    )

    if st.button(
        "Save Night Reflection",
        use_container_width=True,
    ):

        save_night_reflection(
            user_id=user_id,
            reflection=reflection,
        )

        st.success(
            "Night reflection saved!"
        )

        st.rerun()

    st.divider()

    # -------------------------------------------------
    # Sidebar
    # -------------------------------------------------

    with st.sidebar:

        st.markdown("## 🌸 MindEase")

        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
        ):
            navigate("dashboard")

        if st.button(
            "💬 Safe Space",
            use_container_width=True,
        ):
            navigate("safe_space")

        if st.button(
            "😊 Mood Tracker",
            use_container_width=True,
        ):
            navigate("mood")

        if st.button(
            "📔 Journal",
            use_container_width=True,
        ):
            navigate("journal")

        if st.button(
            "📊 Insights",
            use_container_width=True,
        ):
            navigate("insights")

        if st.button(
            "🧠 Memory",
            use_container_width=True,
        ):
            navigate("memory")

        if st.button(
            "📅 Weekly Reports",
            use_container_width=True,
        ):
            navigate("reports")