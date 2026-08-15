"""
Wellness services for MindEase.

Handles wellness activity analysis such as
calculating the user's current activity streak.
"""

from datetime import date, timedelta

from features.mood.services import get_user_moods
from features.journal.services import get_user_journal_entries


# ---------------------------------------------------------
# Activity Dates
# ---------------------------------------------------------

def get_user_activity_dates(
    user_id: str,
) -> set[date]:
    """
    Return all dates on which the user had wellness activity.

    Wellness activity currently includes:
    - Mood check-ins
    - Journal entries
    """

    moods = get_user_moods(user_id)
    journals = get_user_journal_entries(user_id)

    activity_dates: set[date] = set()

    # Mood activity
    for mood in moods:

        if mood.created_at:

            activity_dates.add(
                mood.created_at.date()
            )

    # Journal activity
    for entry in journals:

        if entry.created_at:

            activity_dates.add(
                entry.created_at.date()
            )

    return activity_dates


# ---------------------------------------------------------
# Current Wellness Streak
# ---------------------------------------------------------

def get_wellness_streak(
    user_id: str,
) -> int:
    """
    Calculate the user's current consecutive wellness streak.

    A day counts as active if the user either:
    - records a mood, or
    - creates a journal entry.

    The streak is counted backwards from today.

    If the user has no activity today, the streak is
    considered broken and returns 0.
    """

    activity_dates = get_user_activity_dates(
        user_id
    )

    if not activity_dates:

        return 0

    today = date.today()

    # -----------------------------------------------------
    # User must have activity today
    # -----------------------------------------------------

    if today not in activity_dates:

        return 0

    # -----------------------------------------------------
    # Count consecutive days
    # -----------------------------------------------------

    streak = 0

    current_date = today

    while current_date in activity_dates:

        streak += 1

        current_date -= timedelta(
            days=1
        )

    return streak


# ---------------------------------------------------------
# Wellness Activity Summary
# ---------------------------------------------------------

def get_wellness_activity_summary(
    user_id: str,
) -> dict:
    """
    Return a summary of the user's wellness activity.
    """

    activity_dates = get_user_activity_dates(
        user_id
    )

    today = date.today()

    return {
        "total_active_days": len(activity_dates),
        "active_today": today in activity_dates,
        "current_streak": get_wellness_streak(
            user_id
        ),
    }