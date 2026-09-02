"""
AI Memory Management Page for MindEase.

Allows users to:
- View AI memories
- Add memories
- Edit memories
- Delete memories
- Clear all memories
"""

import streamlit as st

from utils.session import is_logged_in
from ui.navigation import navigate

from features.ai.memory import (
    create_memory,
    get_user_memories,
    update_memory,
    delete_memory,
    clear_user_memories,
)


def show_memory_page():
    """
    Display memory management page.
    """

    # ---------------------------------------------------------
    # Authentication
    # ---------------------------------------------------------

    if not is_logged_in():

        st.error("Please login first.")
        return

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.error(
            "User session not found."
        )
        return

    # ---------------------------------------------------------
    # Header
    # ---------------------------------------------------------

    st.title("🧠 AI Memory Center")

    st.caption(
        "Manage what your AI companion remembers."
    )

    st.divider()

    # ---------------------------------------------------------
    # Add Memory
    # ---------------------------------------------------------

    st.subheader("➕ Add Memory")

    with st.form("create_memory_form"):

        category = st.selectbox(
            "Category",
            [
                "goal",
                "preference",
                "study",
                "project",
                "career",
                "general",
            ],
        )

        content = st.text_area(
            "Memory Content",
            placeholder=(
                "Example: Preparing for product-based company placements."
            ),
        )

        submit = st.form_submit_button(
            "Save Memory"
        )

        if submit:

            if content.strip():

                create_memory(
                    user_id=user_id,
                    content=content,
                    category=category,
                )

                st.success(
                    "Memory saved successfully."
                )

                st.rerun()

            else:

                st.warning(
                    "Memory content cannot be empty."
                )

    st.divider()

    # ---------------------------------------------------------
    # Existing Memories
    # ---------------------------------------------------------

    st.subheader("📚 Stored Memories")

    memories = get_user_memories(
        user_id
    )

    if not memories:

        st.info(
            "No memories stored yet."
        )

    else:

        for memory in memories:

            with st.expander(
                f"[{memory.category}] {memory.content[:50]}"
            ):

                new_category = st.selectbox(
                    "Category",
                    [
                        "goal",
                        "preference",
                        "study",
                        "project",
                        "career",
                        "general",
                    ],
                    index=[
                        "goal",
                        "preference",
                        "study",
                        "project",
                        "career",
                        "general",
                    ].index(memory.category)
                    if memory.category in [
                        "goal",
                        "preference",
                        "study",
                        "project",
                        "career",
                        "general",
                    ]
                    else 5,
                    key=f"cat_{memory.id}",
                )

                new_content = st.text_area(
                    "Content",
                    value=memory.content,
                    key=f"text_{memory.id}",
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "💾 Update",
                        key=f"update_{memory.id}",
                        use_container_width=True,
                    ):

                        update_memory(
                            memory_id=memory.id,
                            user_id=user_id,
                            content=new_content,
                            category=new_category,
                        )

                        st.success(
                            "Memory updated."
                        )

                        st.rerun()

                with col2:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{memory.id}",
                        use_container_width=True,
                    ):

                        delete_memory(
                            memory_id=memory.id,
                            user_id=user_id,
                        )

                        st.success(
                            "Memory deleted."
                        )

                        st.rerun()

    st.divider()

    # ---------------------------------------------------------
    # Clear All Memories
    # ---------------------------------------------------------

    st.subheader("⚠ Memory Cleanup")

    if st.button(
        "🧹 Clear All Memories",
        use_container_width=True,
    ):

        deleted_count = clear_user_memories(
            user_id
        )

        st.success(
            f"Deleted {deleted_count} memories."
        )

        st.rerun()

    st.divider()

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    if st.button(
        "← Back to Dashboard",
        use_container_width=True,
    ):

        navigate("dashboard")