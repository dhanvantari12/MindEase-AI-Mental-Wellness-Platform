"""
Journal service for MindEase.

Handles creating, retrieving, updating, and deleting
journal entries for users.
"""

from sqlalchemy import select

from database.session import get_db
from models.journal import Journal


def create_journal_entry(
    user_id: str,
    title: str,
    content: str,
    mood: str | None = None,
) -> Journal:
    """
    Create and save a new journal entry.
    """

    journal_entry = Journal(
        user_id=user_id,
        title=title.strip(),
        content=content.strip(),
        mood=mood,
    )

    with get_db() as db:
        db.add(journal_entry)
        db.commit()
        db.refresh(journal_entry)

        return journal_entry


def get_user_journal_entries(
    user_id: str,
) -> list[Journal]:
    """
    Return all journal entries for a user.

    Newest entries are returned first.
    """

    with get_db() as db:
        statement = (
            select(Journal)
            .where(Journal.user_id == user_id)
            .order_by(Journal.created_at.desc())
        )

        return list(db.scalars(statement).all())


def get_journal_entry_by_id(
    entry_id: str,
    user_id: str,
) -> Journal | None:
    """
    Return a specific journal entry belonging to a user.
    """

    with get_db() as db:
        statement = (
            select(Journal)
            .where(
                Journal.id == entry_id,
                Journal.user_id == user_id,
            )
        )

        return db.scalar(statement)


def update_journal_entry(
    entry_id: str,
    user_id: str,
    title: str,
    content: str,
    mood: str | None = None,
) -> Journal | None:
    """
    Update an existing journal entry.

    Returns the updated entry, or None if it doesn't exist.
    """

    with get_db() as db:

        statement = (
            select(Journal)
            .where(
                Journal.id == entry_id,
                Journal.user_id == user_id,
            )
        )

        journal_entry = db.scalar(statement)

        if journal_entry is None:
            return None

        journal_entry.title = title.strip()
        journal_entry.content = content.strip()
        journal_entry.mood = mood

        db.commit()
        db.refresh(journal_entry)

        return journal_entry


def delete_journal_entry(
    entry_id: str,
    user_id: str,
) -> bool:
    """
    Delete a journal entry belonging to a user.

    Returns True if deleted, otherwise False.
    """

    with get_db() as db:

        statement = (
            select(Journal)
            .where(
                Journal.id == entry_id,
                Journal.user_id == user_id,
            )
        )

        journal_entry = db.scalar(statement)

        if journal_entry is None:
            return False

        db.delete(journal_entry)
        db.commit()

        return True