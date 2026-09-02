"""
Test MindEase statistics services.
"""

from utils.session import restore_session
from features.statistics.services import (
    get_total_mood_checkins,
    get_mood_distribution,
    get_weekly_mood_counts,
    get_total_journal_entries,
    get_wellness_summary,
)


print("=" * 60)
print("Testing MindEase Statistics")
print("=" * 60)


# ---------------------------------------------------------
# Test user
# ---------------------------------------------------------

USER_ID = "704f4b24-fc91-4d11-b072-b4296d2a8abe"


# ---------------------------------------------------------
# Total mood check-ins
# ---------------------------------------------------------

total_moods = get_total_mood_checkins(
    USER_ID
)

print("\nTotal mood check-ins:")
print(total_moods)


# ---------------------------------------------------------
# Mood distribution
# ---------------------------------------------------------

distribution = get_mood_distribution(
    USER_ID
)

print("\nMood distribution:")

for mood, count in distribution.items():

    print(
        f"{mood}: {count}"
    )


# ---------------------------------------------------------
# Weekly mood counts
# ---------------------------------------------------------

weekly_counts = get_weekly_mood_counts(
    USER_ID
)

print("\nThis week's moods:")

for mood, count in weekly_counts.items():

    print(
        f"{mood}: {count}"
    )


# ---------------------------------------------------------
# Journal count
# ---------------------------------------------------------

journal_count = get_total_journal_entries(
    USER_ID
)

print("\nTotal journal entries:")
print(journal_count)


# ---------------------------------------------------------
# Wellness summary
# ---------------------------------------------------------

summary = get_wellness_summary(
    USER_ID
)

print("\nWellness summary:")
print(summary)


print("\n" + "=" * 60)
print("Statistics service test completed.")
print("=" * 60)