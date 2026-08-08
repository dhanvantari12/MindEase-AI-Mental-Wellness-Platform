"""
Mood service for MindEase.

Handles creating and retrieving mood check-ins.
"""

from datetime import datetime

from sqlalchemy import select

from database.session import get_db
from models.mood import Mood


def create_mood(
    user_id: str,
    mood: str,
    note: str | None = None,
) -> Mood:
    """
    Create and save a new mood check-in.
    """

    mood_entry = Mood(
        user_id=user_id,
        mood=mood,
        note=note.strip() if note else None,
    )

    with get_db() as db:
        db.add(mood_entry)
        db.commit()
        db.refresh(mood_entry)

        return mood_entry


def get_user_moods(
    user_id: str,
) -> list[Mood]:
    """
    Return all mood check-ins for a user.

    Newest moods are returned first.
    """

    with get_db() as db:
        statement = (
            select(Mood)
            .where(Mood.user_id == user_id)
            .order_by(Mood.created_at.desc())
        )

        return list(db.scalars(statement).all())


def get_latest_mood(
    user_id: str,
) -> Mood | None:
    """
    Return the user's most recent mood.
    """

    with get_db() as db:
        statement = (
            select(Mood)
            .where(Mood.user_id == user_id)
            .order_by(Mood.created_at.desc())
            .limit(1)
        )

        return db.scalar(statement)


def get_today_mood(
    user_id: str,
) -> Mood | None:
    """
    Return the user's most recent mood recorded today.

    Returns None if the user has not recorded a mood today.
    """

    today = datetime.now().date()

    with get_db() as db:
        statement = (
            select(Mood)
            .where(
                Mood.user_id == user_id,
                Mood.created_at >= datetime.combine(
                    today,
                    datetime.min.time(),
                ),
                Mood.created_at < datetime.combine(
                    today,
                    datetime.max.time(),
                ),
            )
            .order_by(Mood.created_at.desc())
            .limit(1)
        )

        return db.scalar(statement)