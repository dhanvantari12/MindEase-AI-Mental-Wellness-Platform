"""
Statistics service for MindEase.

Provides wellness statistics based on
mood check-ins and journal entries.
"""

from datetime import datetime, timedelta

from sqlalchemy import select, func

from database.session import get_db
from models.mood import Mood
from models.journal import Journal


# ---------------------------------------------------------
# Mood Statistics
# ---------------------------------------------------------

def get_total_mood_checkins(
    user_id: str,
) -> int:
    """
    Return the total number of mood check-ins
    recorded by the user.
    """

    with get_db() as db:

        statement = (
            select(func.count())
            .select_from(Mood)
            .where(
                Mood.user_id == user_id
            )
        )

        return db.scalar(statement) or 0


def get_mood_distribution(
    user_id: str,
) -> dict[str, int]:
    """
    Return the total count for each mood category.

    All mood categories are included even if
    their count is zero.
    """

    mood_counts = {
        "Great": 0,
        "Good": 0,
        "Okay": 0,
        "Low": 0,
        "Struggling": 0,
    }

    with get_db() as db:

        statement = (
            select(
                Mood.mood,
                func.count(Mood.id),
            )
            .where(
                Mood.user_id == user_id
            )
            .group_by(Mood.mood)
        )

        results = db.execute(statement).all()

    for mood, count in results:

        if mood in mood_counts:
            mood_counts[mood] = count

    return mood_counts


# ---------------------------------------------------------
# Weekly Mood Statistics
# ---------------------------------------------------------

def get_weekly_mood_counts(
    user_id: str,
) -> dict[str, int]:
    """
    Return mood counts for the current week.

    The week starts on Monday.
    """

    today = datetime.now().date()

    start_of_week = (
        today
        - timedelta(
            days=today.weekday()
        )
    )

    start_datetime = datetime.combine(
        start_of_week,
        datetime.min.time(),
    )

    end_datetime = datetime.combine(
        today,
        datetime.max.time(),
    )

    mood_counts = {
        "Great": 0,
        "Good": 0,
        "Okay": 0,
        "Low": 0,
        "Struggling": 0,
    }

    with get_db() as db:

        statement = (
            select(Mood.mood)
            .where(
                Mood.user_id == user_id,
                Mood.created_at >= start_datetime,
                Mood.created_at <= end_datetime,
            )
        )

        moods = db.scalars(
            statement
        ).all()

    for mood in moods:

        if mood in mood_counts:
            mood_counts[mood] += 1

    return mood_counts


# ---------------------------------------------------------
# Journal Statistics
# ---------------------------------------------------------

def get_total_journal_entries(
    user_id: str,
) -> int:
    """
    Return the total number of journal
    entries created by the user.
    """

    with get_db() as db:

        statement = (
            select(func.count())
            .select_from(Journal)
            .where(
                Journal.user_id == user_id
            )
        )

        return db.scalar(statement) or 0


# ---------------------------------------------------------
# Wellness Summary
# ---------------------------------------------------------

def get_wellness_summary(
    user_id: str,
) -> dict:
    """
    Return a combined wellness summary
    for the user.
    """

    mood_distribution = (
        get_mood_distribution(user_id)
    )

    total_moods = sum(
        mood_distribution.values()
    )

    total_journal_entries = (
        get_total_journal_entries(
            user_id
        )
    )

    if total_moods > 0:

        most_frequent_mood = max(
            mood_distribution,
            key=mood_distribution.get,
        )

    else:

        most_frequent_mood = None

    return {
        "total_mood_checkins": total_moods,
        "total_journal_entries": (
            total_journal_entries
        ),
        "mood_distribution": (
            mood_distribution
        ),
        "most_frequent_mood": (
            most_frequent_mood
        ),
    }