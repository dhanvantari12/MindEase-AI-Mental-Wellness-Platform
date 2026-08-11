"""
Reminders page for MindEase.

Allows users to create, view, complete,
edit, and delete personal reminders.
"""

import streamlit as st
from datetime import datetime, date, time

from features.reminders.services import (
    create_reminder,
    get_pending_reminders,
    get_completed_reminders,
    mark_reminder_completed,
    mark_reminder_pending,
    update_reminder,
    delete_reminder,
)

from ui.navigation import navigate
from utils.session import is_logged_in


def show_reminders_page():
    """Display the MindEase Reminders page."""

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
        st.error("User session not found. Please login again.")
        return

    # ---------------------------------------------------------
    # Page Header
    # ---------------------------------------------------------

    st.title("🔔 Reminders")

    st.caption(
        "Stay organized and take care of yourself, one reminder at a time."
    )

    st.write("")

    # ---------------------------------------------------------
    # Sidebar Navigation
    # ---------------------------------------------------------

    with st.sidebar:

        st.markdown("## 🌸 MindEase")

        st.caption("Your wellness companion")

        st.divider()

        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
            key="reminders_dashboard",
        ):
            navigate("dashboard")

        if st.button(
            "💬 Safe Space",
            use_container_width=True,
            key="reminders_safe_space",
        ):
            navigate("safe_space")

        if st.button(
            "😊 Mood Tracker",
            use_container_width=True,
            key="reminders_mood",
        ):
            navigate("mood")

        if st.button(
            "📔 Journal",
            use_container_width=True,
            key="reminders_journal",
        ):
            navigate("journal")

        if st.button(
            "🔔 Reminders",
            use_container_width=True,
            key="reminders_current",
        ):
            st.rerun()

        st.divider()

        if st.button(
            "⬅️ Back to Dashboard",
            use_container_width=True,
            key="reminders_back",
        ):
            navigate("dashboard")

    # ---------------------------------------------------------
    # Create Reminder
    # ---------------------------------------------------------

    st.subheader("➕ Create a Reminder")

    with st.form("create_reminder_form"):

        title = st.text_input(
            "Reminder title",
            placeholder="Example: Take a short break",
        )

        description = st.text_area(
            "Description",
            placeholder="Example: Step away from the screen and relax.",
        )

        reminder_date = st.date_input(
            "Date",
            value=date.today(),
            min_value=date.today(),
        )

        reminder_time = st.time_input(
            "Time",
            value=time(hour=9, minute=0),
        )

        create_button = st.form_submit_button(
            "➕ Add Reminder",
            use_container_width=True,
        )

        if create_button:

            if not title.strip():

                st.error(
                    "Please enter a reminder title."
                )

            else:

                reminder_datetime = datetime.combine(
                    reminder_date,
                    reminder_time,
                )

                if reminder_datetime < datetime.now():

                    st.error(
                        "Please select a future date and time."
                    )

                else:

                    create_reminder(
                        user_id=user_id,
                        title=title,
                        description=description,
                        reminder_time=reminder_datetime,
                    )

                    st.success(
                        "✅ Reminder created successfully!"
                    )

                    st.rerun()

    st.divider()

    # ---------------------------------------------------------
    # Pending Reminders
    # ---------------------------------------------------------

    st.subheader("📋 Upcoming Reminders")

    pending_reminders = get_pending_reminders(
        user_id
    )

    if not pending_reminders:

        st.info(
            "🌸 You don't have any pending reminders."
        )

    else:

        for reminder in pending_reminders:

            with st.container(border=True):

                col1, col2 = st.columns(
                    [4, 1]
                )

                with col1:

                    st.markdown(
                        f"### 🔔 {reminder.title}"
                    )

                    if reminder.description:

                        st.write(
                            reminder.description
                        )

                    st.caption(
                        "📅 "
                        + reminder.reminder_time.strftime(
                            "%d %B %Y"
                        )
                        + " • ⏰ "
                        + reminder.reminder_time.strftime(
                            "%I:%M %p"
                        )
                    )

                with col2:

                    if st.button(
                        "✅ Done",
                        use_container_width=True,
                        key=f"complete_{reminder.id}",
                    ):

                        mark_reminder_completed(
                            reminder.id,
                            user_id,
                        )

                        st.success(
                            "Reminder completed!"
                        )

                        st.rerun()

                # -------------------------------------------------
                # Edit / Delete
                # -------------------------------------------------

                edit_col, delete_col = st.columns(2)

                with edit_col:

                    if st.button(
                        "✏️ Edit",
                        use_container_width=True,
                        key=f"edit_{reminder.id}",
                    ):

                        st.session_state[
                            f"editing_reminder_{reminder.id}"
                        ] = True

                        st.rerun()

                with delete_col:

                    if st.button(
                        "🗑️ Delete",
                        use_container_width=True,
                        key=f"delete_{reminder.id}",
                    ):

                        delete_reminder(
                            reminder.id,
                            user_id,
                        )

                        st.success(
                            "Reminder deleted."
                        )

                        st.rerun()

                # -------------------------------------------------
                # Edit Form
                # -------------------------------------------------

                if st.session_state.get(
                    f"editing_reminder_{reminder.id}",
                    False,
                ):

                    st.markdown(
                        "#### ✏️ Edit Reminder"
                    )

                    edit_title = st.text_input(
                        "Title",
                        value=reminder.title,
                        key=f"edit_title_{reminder.id}",
                    )

                    edit_description = st.text_area(
                        "Description",
                        value=reminder.description or "",
                        key=f"edit_description_{reminder.id}",
                    )

                    edit_date = st.date_input(
                        "Date",
                        value=reminder.reminder_time.date(),
                        min_value=date.today(),
                        key=f"edit_date_{reminder.id}",
                    )

                    edit_time = st.time_input(
                        "Time",
                        value=reminder.reminder_time.time(),
                        key=f"edit_time_{reminder.id}",
                    )

                    save_col, cancel_col = st.columns(2)

                    with save_col:

                        if st.button(
                            "💾 Save Changes",
                            use_container_width=True,
                            key=f"save_edit_{reminder.id}",
                        ):

                            if not edit_title.strip():

                                st.error(
                                    "Title cannot be empty."
                                )

                            else:

                                updated_datetime = datetime.combine(
                                    edit_date,
                                    edit_time,
                                )

                                update_reminder(
                                    reminder_id=reminder.id,
                                    user_id=user_id,
                                    title=edit_title,
                                    description=edit_description,
                                    reminder_time=updated_datetime,
                                )

                                st.session_state[
                                    f"editing_reminder_{reminder.id}"
                                ] = False

                                st.success(
                                    "Reminder updated successfully!"
                                )

                                st.rerun()

                    with cancel_col:

                        if st.button(
                            "❌ Cancel",
                            use_container_width=True,
                            key=f"cancel_edit_{reminder.id}",
                        ):

                            st.session_state[
                                f"editing_reminder_{reminder.id}"
                            ] = False

                            st.rerun()

    st.divider()

    # ---------------------------------------------------------
    # Completed Reminders
    # ---------------------------------------------------------

    st.subheader("✅ Completed Reminders")

    completed_reminders = get_completed_reminders(
        user_id
    )

    if not completed_reminders:

        st.caption(
            "No completed reminders yet."
        )

    else:

        for reminder in completed_reminders:

            with st.container(border=True):

                col1, col2 = st.columns(
                    [4, 1]
                )

                with col1:

                    st.markdown(
                        f"### ✅ {reminder.title}"
                    )

                    if reminder.description:

                        st.write(
                            reminder.description
                        )

                    st.caption(
                        "📅 "
                        + reminder.reminder_time.strftime(
                            "%d %B %Y"
                        )
                        + " • ⏰ "
                        + reminder.reminder_time.strftime(
                            "%I:%M %p"
                        )
                    )

                with col2:

                    if st.button(
                        "↩️ Pending",
                        use_container_width=True,
                        key=f"pending_{reminder.id}",
                    ):

                        mark_reminder_pending(
                            reminder.id,
                            user_id,
                        )

                        st.success(
                            "Reminder moved back to pending."
                        )

                        st.rerun()