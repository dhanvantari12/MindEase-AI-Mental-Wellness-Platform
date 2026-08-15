"""
Profile page for MindEase.

Displays user profile information and wellness activity.
Allows the user to update their full name.
"""

import streamlit as st

from sqlalchemy import select

from database.session import get_db
from models.user import User

from features.mood.services import get_user_moods
from features.journal.services import get_user_journal_entries
from features.reminders.services import get_user_reminders
from features.insights.services import calculate_wellness_score

from ui.navigation import navigate
from utils.session import is_logged_in
from ui.components.logout_button import logout_button


def show_profile_page():
    """Display the MindEase profile page."""

    # ---------------------------------------------------------
    # Authentication check
    # ---------------------------------------------------------

    if not is_logged_in():

        st.error("Please login first.")

        return

    # ---------------------------------------------------------
    # Get current user ID
    # ---------------------------------------------------------

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.error(
            "User session not found. Please login again."
        )

        return

    # ---------------------------------------------------------
    # Get current user from database
    # ---------------------------------------------------------

    with get_db() as db:

        statement = (
            select(User)
            .where(User.id == user_id)
        )

        user = db.scalar(statement)

    if user is None:

        st.error(
            "Unable to load your profile."
        )

        return

    # ---------------------------------------------------------
    # Load wellness information
    # ---------------------------------------------------------

    moods = get_user_moods(user_id)

    journal_entries = get_user_journal_entries(
        user_id
    )

    reminders = get_user_reminders(
        user_id
    )

    wellness_score = calculate_wellness_score(
        user_id
    )

    # ---------------------------------------------------------
    # Page Header
    # ---------------------------------------------------------

    st.title("👤 My Profile")

    st.caption(
        "Manage your profile and view your wellness activity."
    )

    st.write("")

    # ---------------------------------------------------------
    # Profile Header
    # ---------------------------------------------------------

    profile_col1, profile_col2 = st.columns(
        [1, 3]
    )

    with profile_col1:

        if user.profile_image:

            st.image(
                user.profile_image,
                width=140,
            )

        else:

            st.markdown(
                """
                <div style="
                    width:120px;
                    height:120px;
                    border-radius:50%;
                    background:#e8f5f2;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:55px;
                    margin-bottom:10px;
                ">
                    👤
                </div>
                """,
                unsafe_allow_html=True,
            )

    with profile_col2:

        st.subheader(
            user.full_name
        )

        st.caption(
            f"📧 {user.email}"
        )

        st.caption(
            "🌸 MindEase Member"
        )

    st.write("")

    st.divider()

    # ---------------------------------------------------------
    # Personal Information
    # ---------------------------------------------------------

    st.subheader(
        "📝 Personal Information"
    )

    with st.form(
        "profile_form"
    ):

        full_name = st.text_input(
            "Full Name",
            value=user.full_name,
            max_chars=100,
        )

        email = st.text_input(
            "Email",
            value=user.email,
            disabled=True,
        )

        st.caption(
            "Email address cannot be changed here."
        )

        save_profile = st.form_submit_button(
            "💾 Save Changes",
            use_container_width=True,
        )

        if save_profile:

            full_name = full_name.strip()

            if not full_name:

                st.error(
                    "Full name cannot be empty."
                )

            else:

                with get_db() as db:

                    statement = (
                        select(User)
                        .where(User.id == user_id)
                    )

                    current_user = db.scalar(
                        statement
                    )

                    if current_user:

                        current_user.full_name = (
                            full_name
                        )

                        db.commit()

                # Update Streamlit session
                st.session_state.user_name = (
                    full_name
                )

                st.success(
                    "✅ Profile updated successfully!"
                )

                st.rerun()

    st.divider()

    # ---------------------------------------------------------
    # Wellness Overview
    # ---------------------------------------------------------

    st.subheader(
        "🌸 Wellness Overview"
    )

    stat_col1, stat_col2, stat_col3, stat_col4 = (
        st.columns(4)
    )

    with stat_col1:

        st.metric(
            label="😊 Mood Check-ins",
            value=len(moods),
        )

    with stat_col2:

        st.metric(
            label="📔 Journal Entries",
            value=len(journal_entries),
        )

    with stat_col3:

        st.metric(
            label="🔔 Reminders",
            value=len(reminders),
        )

    with stat_col4:

        st.metric(
            label="💡 Wellness Score",
            value=f"{wellness_score}/100",
        )

    st.write("")

    # ---------------------------------------------------------
    # Account Information
    # ---------------------------------------------------------

    st.subheader(
        "📋 Account Information"
    )

    account_col1, account_col2 = st.columns(2)

    with account_col1:

        st.write("**Account ID**")

        st.code(
            str(user.id)
        )

    with account_col2:

        st.write("**Member Since**")

        if getattr(
            user,
            "created_at",
            None,
        ):

            created_at = user.created_at

            st.write(
                created_at.strftime(
                    "%d %B %Y"
                )
            )

        else:

            st.write(
                "Not available"
            )

    st.divider()

    # ---------------------------------------------------------
    # Quick Actions
    # ---------------------------------------------------------

    st.subheader(
        "🚀 Quick Actions"
    )

    action_col1, action_col2, action_col3 = (
        st.columns(3)
    )

    with action_col1:

        if st.button(
            "😊 Mood Tracker",
            use_container_width=True,
            key="profile_mood_button",
        ):

            navigate("mood")

    with action_col2:

        if st.button(
            "📔 Journal",
            use_container_width=True,
            key="profile_journal_button",
        ):

            navigate("journal")

    with action_col3:

        if st.button(
            "💡 Insights",
            use_container_width=True,
            key="profile_insights_button",
        ):

            navigate("insights")

    st.write("")

    st.divider()

    # ---------------------------------------------------------
    # Sidebar Navigation
    # ---------------------------------------------------------

    with st.sidebar:

        st.markdown(
            "## 🌸 MindEase"
        )

        st.caption(
            "Your wellness companion"
        )

        st.divider()

        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
            key="profile_sidebar_dashboard",
        ):

            navigate("dashboard")

        if st.button(
            "💬 Safe Space",
            use_container_width=True,
            key="profile_sidebar_safe_space",
        ):

            navigate("safe_space")

        if st.button(
            "😊 Mood Tracker",
            use_container_width=True,
            key="profile_sidebar_mood",
        ):

            navigate("mood")

        if st.button(
            "📔 Journal",
            use_container_width=True,
            key="profile_sidebar_journal",
        ):

            navigate("journal")

        if st.button(
            "🔔 Reminders",
            use_container_width=True,
            key="profile_sidebar_reminders",
        ):

            navigate("reminders")

        if st.button(
            "💡 Insights",
            use_container_width=True,
            key="profile_sidebar_insights",
        ):

            navigate("insights")

        if st.button(
            "📊 Statistics",
            use_container_width=True,
            key="profile_sidebar_statistics",
        ):

            navigate("statistics")

        st.divider()

        if st.button(
            "👤 Profile",
            use_container_width=True,
            key="profile_sidebar_profile",
        ):

            st.rerun()

        if st.button(
            "⚙️ Settings",
            use_container_width=True,
            key="profile_sidebar_settings",
        ):

            st.info(
                "Settings are coming soon."
            )

        st.divider()

        logout_button()

    # ---------------------------------------------------------
    # Disclaimer
    # ---------------------------------------------------------

    st.caption(
        "💙 MindEase wellness information is intended "
        "for self-reflection and personal wellness tracking. "
        "It is not a medical diagnosis."
    )