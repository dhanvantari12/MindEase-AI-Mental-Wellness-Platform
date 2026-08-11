"""
Reminder services for MindEase.

Handles creating, retrieving, updating, completing,
and deleting reminders for users.
"""

from datetime import datetime

from sqlalchemy import select

from database.session import get_db
from models.reminder import Reminder


def create_reminder(
    user_id: str,
    title: str,
    reminder_time: datetime,
    description: str | None = None,
) -> Reminder:
    """
    Create and save a new reminder.
    """

    reminder = Reminder(
        user_id=user_id,
        title=title.strip(),
        description=(
            description.strip()
            if description
            else None
        ),
        reminder_time=reminder_time,
        completed=False,
    )

    with get_db() as db:

        db.add(reminder)

        db.commit()

        db.refresh(reminder)

        return reminder


def get_user_reminders(
    user_id: str,
) -> list[Reminder]:
    """
    Return all reminders belonging to a user.

    Newest reminder times are returned first.
    """

    with get_db() as db:

        statement = (
            select(Reminder)
            .where(
                Reminder.user_id == user_id
            )
            .order_by(
                Reminder.reminder_time.asc()
            )
        )

        return list(
            db.scalars(statement).all()
        )


def get_pending_reminders(
    user_id: str,
) -> list[Reminder]:
    """
    Return incomplete reminders for a user.

    Reminders are ordered by their scheduled time.
    """

    with get_db() as db:

        statement = (
            select(Reminder)
            .where(
                Reminder.user_id == user_id,
                Reminder.completed.is_(False),
            )
            .order_by(
                Reminder.reminder_time.asc()
            )
        )

        return list(
            db.scalars(statement).all()
        )


def get_completed_reminders(
    user_id: str,
) -> list[Reminder]:
    """
    Return completed reminders for a user.
    """

    with get_db() as db:

        statement = (
            select(Reminder)
            .where(
                Reminder.user_id == user_id,
                Reminder.completed.is_(True),
            )
            .order_by(
                Reminder.reminder_time.desc()
            )
        )

        return list(
            db.scalars(statement).all()
        )


def get_reminder_by_id(
    reminder_id: str,
    user_id: str,
) -> Reminder | None:
    """
    Return a specific reminder belonging to a user.
    """

    with get_db() as db:

        statement = (
            select(Reminder)
            .where(
                Reminder.id == reminder_id,
                Reminder.user_id == user_id,
            )
        )

        return db.scalar(statement)


def mark_reminder_completed(
    reminder_id: str,
    user_id: str,
) -> bool:
    """
    Mark a reminder as completed.

    Returns True if successful, otherwise False.
    """

    with get_db() as db:

        statement = (
            select(Reminder)
            .where(
                Reminder.id == reminder_id,
                Reminder.user_id == user_id,
            )
        )

        reminder = db.scalar(statement)

        if reminder is None:
            return False

        reminder.completed = True

        db.commit()

        return True


def mark_reminder_pending(
    reminder_id: str,
    user_id: str,
) -> bool:
    """
    Mark a completed reminder as pending again.

    Returns True if successful, otherwise False.
    """

    with get_db() as db:

        statement = (
            select(Reminder)
            .where(
                Reminder.id == reminder_id,
                Reminder.user_id == user_id,
            )
        )

        reminder = db.scalar(statement)

        if reminder is None:
            return False

        reminder.completed = False

        db.commit()

        return True


def update_reminder(
    reminder_id: str,
    user_id: str,
    title: str,
    reminder_time: datetime,
    description: str | None = None,
) -> Reminder | None:
    """
    Update an existing reminder.

    Returns the updated reminder,
    or None if it does not exist.
    """

    with get_db() as db:

        statement = (
            select(Reminder)
            .where(
                Reminder.id == reminder_id,
                Reminder.user_id == user_id,
            )
        )

        reminder = db.scalar(statement)

        if reminder is None:
            return None

        reminder.title = title.strip()

        reminder.description = (
            description.strip()
            if description
            else None
        )

        reminder.reminder_time = reminder_time

        db.commit()

        db.refresh(reminder)

        return reminder


def delete_reminder(
    reminder_id: str,
    user_id: str,
) -> bool:
    """
    Delete a reminder belonging to a user.

    Returns True if deleted,
    otherwise False.
    """

    with get_db() as db:

        statement = (
            select(Reminder)
            .where(
                Reminder.id == reminder_id,
                Reminder.user_id == user_id,
            )
        )

        reminder = db.scalar(statement)

        if reminder is None:
            return False

        db.delete(reminder)

        db.commit()

        return True