import streamlit as st

from features.reminders.services import (
    get_today_checkin,
    save_morning_checkin,
    save_night_reflection,
)

from features.checkins.streaks import (
    get_current_streak,
    get_longest_streak,
)

from utils.session import is_logged_in
from ui.navigation import navigate


def show_checkins_page():

    if not is_logged_in():

        st.error(
            "Please login first."
        )

        return

    user_id = st.session_state.get(
        "user_id"
    )

    if not user_id:

        st.error(
            "User session not found."
        )

        return

    checkin = get_today_checkin(
        user_id
    )

    st.title(
        "🌞 Daily Wellness Check-In"
    )

    st.caption(
        "Start and end your day with reflection."
    )

    st.divider()

    current_streak = get_current_streak(
        user_id
    )

    longest_streak = get_longest_streak(
        user_id
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🔥 Current Streak",
            current_streak,
        )

    with col2:

        st.metric(
            "🏆 Longest Streak",
            longest_streak,
        )

    st.divider()

    st.subheader(
        "🌞 Morning Mood"
    )

    current_mood = (
        checkin.morning_mood
        if checkin
        else None
    )

    mood = st.selectbox(
        "How are you feeling today?",
        [
            "Great",
            "Good",
            "Okay",
            "Low",
            "Struggling",
        ],
        index=(
            [
                "Great",
                "Good",
                "Okay",
                "Low",
                "Struggling",
            ].index(current_mood)
            if current_mood
            else 1
        ),
    )

    if st.button(
        "Save Morning Check-In",
        use_container_width=True,
    ):

        save_morning_checkin(
            user_id,
            mood,
        )

        st.success(
            "Morning mood saved."
        )

        st.rerun()

    st.divider()

    st.subheader(
        "🌙 Night Reflection"
    )

    current_reflection = (
        checkin.night_reflection
        if checkin
        and checkin.night_reflection
        else ""
    )

    reflection = st.text_area(
        "What went well today?",
        value=current_reflection,
        height=150,
    )

    if st.button(
        "Save Night Reflection",
        use_container_width=True,
    ):

        save_night_reflection(
            user_id,
            reflection,
        )

        st.success(
            "Reflection saved."
        )

        st.rerun()

    st.divider()

    with st.sidebar:

        st.markdown(
            "## 🌸 MindEase"
        )

        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
        ):
            navigate("dashboard")

        if st.button(
            "🌞 Daily Check-In",
            use_container_width=True,
        ):
            st.rerun()

        if st.button(
            "💬 Safe Space",
            use_container_width=True,
        ):
            navigate("safe_space")

        if st.button(
            "📊 Insights",
            use_container_width=True,
        ):
            navigate("insights")