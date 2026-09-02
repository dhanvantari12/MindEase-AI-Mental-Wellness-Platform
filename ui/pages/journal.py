"""
Journal page for MindEase.
"""

import streamlit as st

from features.journal.services import (
    create_journal_entry,
    get_user_journal_entries,
    update_journal_entry,
    delete_journal_entry,
)

from ui.navigation import navigate
from utils.session import is_logged_in

from features.journal.pdf_export import (
    export_journal_pdf,
)


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
    # Edit mode state
    # ---------------------------------------------------------

    editing_entry_id = st.session_state.get(
        "editing_entry_id"
    )

    # ---------------------------------------------------------
    # New Journal Entry
    # ---------------------------------------------------------

    if editing_entry_id is None:

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

        # -----------------------------------------------------
        # Save Entry
        # -----------------------------------------------------

        if st.button(
            "💾 Save Journal Entry",
            use_container_width=True,
        ):

            if not title.strip():
                st.warning("Please enter a title.")

            elif not content.strip():
                st.warning(
                    "Please write something before saving."
                )

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
    # Edit Existing Entry
    # ---------------------------------------------------------

    else:

        entry = next(
            (
                journal_entry
                for journal_entry
                in get_user_journal_entries(user_id)
                if journal_entry.id == editing_entry_id
            ),
            None,
        )

        if entry is None:

            st.error(
                "Journal entry could not be found."
            )

            st.session_state.pop(
                "editing_entry_id",
                None,
            )

            st.rerun()

        else:

            st.subheader("✏️ Edit Journal Entry")

            edit_title = st.text_input(
                "Title",
                value=entry.title,
            )

            edit_content = st.text_area(
                "What's on your mind?",
                value=entry.content,
                height=200,
            )

            mood_options = {
                "😄 Great": "Great",
                "🙂 Good": "Good",
                "😐 Okay": "Okay",
                "😔 Low": "Low",
                "😞 Struggling": "Struggling",
            }

            mood_labels = list(mood_options.keys())

            if entry.mood:

                current_mood_label = next(
                    (
                        label
                        for label, value
                        in mood_options.items()
                        if value == entry.mood
                    ),
                    "Not selected",
                )

            else:

                current_mood_label = "Not selected"

            selected_edit_mood = st.selectbox(
                "How are you feeling?",
                options=["Not selected"] + mood_labels,
                index=(
                    ["Not selected"] + mood_labels
                ).index(current_mood_label),
            )

            if selected_edit_mood == "Not selected":
                edit_mood = None
            else:
                edit_mood = mood_options[
                    selected_edit_mood
                ]

            st.write("")

            edit_col1, edit_col2 = st.columns(2)

            # Save changes
            with edit_col1:

                if st.button(
                    "💾 Save Changes",
                    use_container_width=True,
                ):

                    if not edit_title.strip():

                        st.warning(
                            "Please enter a title."
                        )

                    elif not edit_content.strip():

                        st.warning(
                            "Please write something before saving."
                        )

                    else:

                        updated_entry = update_journal_entry(
                            entry_id=entry.id,
                            user_id=user_id,
                            title=edit_title,
                            content=edit_content,
                            mood=edit_mood,
                        )

                        if updated_entry:

                            st.session_state.pop(
                                "editing_entry_id",
                                None,
                            )

                            st.success(
                                "📔 Journal entry updated successfully!"
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Unable to update this journal entry."
                            )

            # Cancel editing
            with edit_col2:

                if st.button(
                    "❌ Cancel",
                    use_container_width=True,
                ):

                    st.session_state.pop(
                        "editing_entry_id",
                        None,
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
                        f"**Mood:** "
                        f"{mood_emoji} {entry.mood}"
                    )

                st.write("")

                action_col1, action_col2 = st.columns(2)

                # -------------------------------------------------
                # Edit button
                # -------------------------------------------------

                with action_col1:

                    if st.button(
                        "✏️ Edit",
                        key=f"edit_{entry.id}",
                        use_container_width=True,
                    ):

                        st.session_state.editing_entry_id = (
                            entry.id
                        )

                        st.rerun()

                # -------------------------------------------------
                # Delete button
                # -------------------------------------------------

                with action_col2:

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{entry.id}",
                        use_container_width=True,
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
    # Export Journal PDF
    # ---------------------------------------------------------

    st.divider()

    st.subheader(
        "📄 Export Journal"
    )

    st.caption(
        "Download all your journal entries as a PDF."
    )

    if st.button(
        "📥 Generate Journal PDF",
        use_container_width=True,
    ):

        pdf_path = (
            "storage/journal_export.pdf"
        )

        export_journal_pdf(
            user_id,
            pdf_path,
        )

        with open(
            pdf_path,
            "rb",
        ) as pdf_file:

            st.download_button(
                label="⬇ Download PDF",
                data=pdf_file,
                file_name="MindEase_Journal.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    # ---------------------------------------------------------
    # Back to Dashboard
    # ---------------------------------------------------------

    st.write("")

    if st.button(
        "← Back to Dashboard",
        use_container_width=True,
    ):

        st.session_state.pop(
            "editing_entry_id",
            None,
        )

        navigate("dashboard")
        

