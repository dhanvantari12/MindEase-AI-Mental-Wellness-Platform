"""
Insights services for MindEase.

Generates simple wellness insights based on
the user's mood and journal activity.
"""

from collections import Counter
from datetime import datetime, timedelta

from features.mood.services import get_user_moods
from features.journal.services import get_user_journal_entries


# ---------------------------------------------------------
# Mood Analysis
# ---------------------------------------------------------

def get_mood_summary(user_id: str) -> dict:
    """
    Return a summary of the user's mood history.
    """

    moods = get_user_moods(user_id)

    if not moods:
        return {
            "total_checkins": 0,
            "most_common_mood": None,
            "mood_counts": {},
            "latest_mood": None,
        }

    mood_values = [
        mood.mood
        for mood in moods
    ]

    mood_counts = Counter(mood_values)

    most_common_mood = (
        mood_counts.most_common(1)[0][0]
        if mood_counts
        else None
    )

    latest_mood = moods[0].mood

    return {
        "total_checkins": len(moods),
        "most_common_mood": most_common_mood,
        "mood_counts": dict(mood_counts),
        "latest_mood": latest_mood,
    }


# ---------------------------------------------------------
# Weekly Mood Analysis
# ---------------------------------------------------------

def get_weekly_mood_summary(user_id: str) -> dict:
    """
    Analyze mood activity during the current week.
    """

    moods = get_user_moods(user_id)

    today = datetime.now().date()

    start_of_week = (
        today
        - timedelta(days=today.weekday())
    )

    weekly_moods = [
        mood
        for mood in moods
        if mood.created_at.date() >= start_of_week
    ]

    mood_counts = Counter(
        mood.mood
        for mood in weekly_moods
    )

    return {
        "total_checkins": len(weekly_moods),
        "mood_counts": dict(mood_counts),
        "most_common_mood": (
            mood_counts.most_common(1)[0][0]
            if mood_counts
            else None
        ),
    }


# ---------------------------------------------------------
# Journal Analysis
# ---------------------------------------------------------

def get_journal_summary(user_id: str) -> dict:
    """
    Return a summary of the user's journal activity.
    """

    entries = get_user_journal_entries(user_id)

    if not entries:
        return {
            "total_entries": 0,
            "latest_entry": None,
        }

    return {
        "total_entries": len(entries),
        "latest_entry": entries[0],
    }


# ---------------------------------------------------------
# Wellness Score
# ---------------------------------------------------------

def calculate_wellness_score(user_id: str) -> int:
    """
    Calculate a simple wellness engagement score.

    The score is based on:
    - Mood check-ins
    - Journal entries
    - Recent activity

    This is an engagement indicator, NOT a medical score.
    """

    moods = get_user_moods(user_id)
    journals = get_user_journal_entries(user_id)

    score = 0

    # Mood activity
    score += min(
        len(moods) * 5,
        40,
    )

    # Journal activity
    score += min(
        len(journals) * 10,
        30,
    )

    # Recent mood activity
    today = datetime.now().date()

    recent_moods = [
        mood
        for mood in moods
        if (
            today
            - mood.created_at.date()
        ).days <= 7
    ]

    if recent_moods:
        score += 20

    # Recent journal activity
    recent_journals = [
        entry
        for entry in journals
        if (
            today
            - entry.created_at.date()
        ).days <= 7
    ]

    if recent_journals:
        score += 10

    return min(score, 100)


# ---------------------------------------------------------
# Generate Insight Messages
# ---------------------------------------------------------

def generate_wellness_insights(user_id: str) -> list[str]:
    """
    Generate simple personalized wellness insights.
    """

    insights = []

    mood_summary = get_mood_summary(user_id)
    journal_summary = get_journal_summary(user_id)

    # -----------------------------------------------------
    # No activity
    # -----------------------------------------------------

    if (
        mood_summary["total_checkins"] == 0
        and journal_summary["total_entries"] == 0
    ):
        insights.append(
            "🌱 Start by recording your mood or writing "
            "your first journal entry."
        )

        return insights

    # -----------------------------------------------------
    # Mood insight
    # -----------------------------------------------------

    most_common_mood = (
        mood_summary["most_common_mood"]
    )

    if most_common_mood:

        insights.append(
            f"😊 Your most frequently recorded mood "
            f"is **{most_common_mood}**."
        )

    # -----------------------------------------------------
    # Mood activity
    # -----------------------------------------------------

    mood_count = mood_summary[
        "total_checkins"
    ]

    if mood_count >= 7:

        insights.append(
            "📈 You've been consistently checking in "
            "with your emotions. Keep it up!"
        )

    elif mood_count >= 3:

        insights.append(
            "🌸 You're building a good habit of "
            "checking in with yourself."
        )

    else:

        insights.append(
            "💙 Try checking in with your mood regularly "
            "to understand your emotional patterns."
        )

    # -----------------------------------------------------
    # Journal insight
    # -----------------------------------------------------

    journal_count = journal_summary[
        "total_entries"
    ]

    if journal_count >= 5:

        insights.append(
            "📔 You've been using journaling regularly. "
            "Writing your thoughts can help with reflection."
        )

    elif journal_count > 0:

        insights.append(
            "✍️ You've started journaling. "
            "Consider making it part of your routine."
        )

    else:

        insights.append(
            "📝 Try writing a journal entry about "
            "how your day went."
        )

    return insights


# ---------------------------------------------------------
# Complete Insights
# ---------------------------------------------------------

def get_user_insights(user_id: str) -> dict:
    """
    Return all wellness insights for a user.

    This function acts as the main service used
    by the Insights UI.
    """

    mood_summary = get_mood_summary(
        user_id
    )

    weekly_summary = get_weekly_mood_summary(
        user_id
    )

    journal_summary = get_journal_summary(
        user_id
    )

    wellness_score = calculate_wellness_score(
        user_id
    )

    insights = generate_wellness_insights(
        user_id
    )

    return {
        "mood_summary": mood_summary,
        "weekly_summary": weekly_summary,
        "journal_summary": journal_summary,
        "wellness_score": wellness_score,
        "insights": insights,
    }