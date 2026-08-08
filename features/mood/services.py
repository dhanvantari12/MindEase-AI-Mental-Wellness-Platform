"""
Mood service for MindEase.

Handles creating and retrieving mood check-ins.
"""

from datetime import datetime, timedelta

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

def get_weekly_mood_counts(
    user_id: str,
) -> dict[str, int]:
    """
    Return the user's mood counts for the current week.

    The week starts on Monday and ends on Sunday.
    """

    today = datetime.now().date()

    # Monday = 0, Sunday = 6
    start_of_week = (
        today
        - timedelta(days=today.weekday())
    )

    start_datetime = datetime.combine(
        start_of_week,
        datetime.min.time(),
    )

    end_datetime = datetime.combine(
        today,
        datetime.max.time(),
    )

    with get_db() as db:

        statement = (
            select(Mood.mood)
            .where(
                Mood.user_id == user_id,
                Mood.created_at >= start_datetime,
                Mood.created_at <= end_datetime,
            )
        )

        moods = db.scalars(statement).all()

    # Keep all mood categories even if their count is zero.
    mood_counts = {
        "Great": 0,
        "Good": 0,
        "Okay": 0,
        "Low": 0,
        "Struggling": 0,
    }

    for mood in moods:
        if mood in mood_counts:
            mood_counts[mood] += 1

    return mood_counts