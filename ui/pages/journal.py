"""
Journal page for MindEase.
"""

import streamlit as st

from features.journal.services import (
    create_journal_entry,
    get_user_journal_entries,
    delete_journal_entry,
)

from ui.navigation import navigate
from utils.session import is_logged_in


def show_journal_page():
    """Display the MindEase journal page."""

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

    # ---------------------------------------------------------
    # Page Header
    # ---------------------------------------------------------

    st.title("📔 Journal")

    st.caption(
        "A private space to write, reflect and understand yourself."
    )

    st.write("")

    # ---------------------------------------------------------
    # New Journal Entry
    # ---------------------------------------------------------

    st.subheader("✍️ Write Something")

    title = st.text_input(
        "Title",
        placeholder="Give your entry a title..."
    )

    content = st.text_area(
        "What's on your mind?",
        placeholder=(
            "Write freely. This is your private space..."
        ),
        height=200,
    )

    mood_options = {
        "😄 Great": "Great",
        "🙂 Good": "Good",
        "😐 Okay": "Okay",
        "😔 Low": "Low",
        "😞 Struggling": "Struggling",
    }

    selected_mood = st.selectbox(
        "How are you feeling?",
        options=["Not selected"] + list(mood_options.keys()),
    )

    if selected_mood == "Not selected":
        mood_value = None
    else:
        mood_value = mood_options[selected_mood]

    st.write("")

    # ---------------------------------------------------------
    # Save Entry
    # ---------------------------------------------------------

    if st.button(
        "💾 Save Journal Entry",
        use_container_width=True,
    ):

        if not title.strip():
            st.warning("Please enter a title.")

        elif not content.strip():
            st.warning("Please write something before saving.")

        else:

            entry = create_journal_entry(
                user_id=user_id,
                title=title,
                content=content,
                mood=mood_value,
            )

            st.success(
                f"📔 '{entry.title}' has been saved successfully!"
            )

            st.rerun()

    # ---------------------------------------------------------
    # Journal History
    # ---------------------------------------------------------

    st.divider()

    st.subheader("📖 Your Journal")

    entries = get_user_journal_entries(user_id)

    if not entries:

        st.info(
            "You haven't written any journal entries yet. "
            "Your thoughts will appear here."
        )

    else:

        for entry in entries:

            mood_emojis = {
                "Great": "😄",
                "Good": "🙂",
                "Okay": "😐",
                "Low": "😔",
                "Struggling": "😞",
            }

            mood_emoji = mood_emojis.get(
                entry.mood,
                "📝",
            )

            with st.expander(
                f"{mood_emoji} {entry.title}"
            ):

                st.caption(
                    entry.created_at.strftime(
                        "%d %B %Y, %I:%M %p"
                    )
                )

                st.write(entry.content)

                if entry.mood:
                    st.write(
                        f"**Mood:** {mood_emoji} {entry.mood}"
                    )

                st.write("")

                if st.button(
                    "🗑️ Delete Entry",
                    key=f"delete_{entry.id}",
                ):

                    deleted = delete_journal_entry(
                        entry_id=entry.id,
                        user_id=user_id,
                    )

                    if deleted:
                        st.success(
                            "Journal entry deleted."
                        )
                        st.rerun()

                    else:
                        st.error(
                            "Unable to delete this entry."
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