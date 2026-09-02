"""
Test Wellness Services for MindEase.
"""

from features.auth.services import get_user_by_email
from features.wellness.services import (
    get_user_activity_dates,
    get_wellness_streak,
    get_wellness_activity_summary,
)


# ---------------------------------------------------------
# Test User
# ---------------------------------------------------------

email = "reminder_test@mindease.com"

user = get_user_by_email(email)


print("=" * 60)
print("Testing MindEase Wellness Services")
print("=" * 60)


if user is None:

    print(
        "❌ Test user not found."
    )

    print(
        "Please create/login with a test user first."
    )

    raise SystemExit


print("\nUser:")
print(user.full_name)
print(user.email)


# ---------------------------------------------------------
# Activity Dates
# ---------------------------------------------------------

activity_dates = get_user_activity_dates(
    user.id
)

print("\nActivity Dates:")

if activity_dates:

    for activity_date in sorted(
        activity_dates,
        reverse=True,
    ):

        print(
            f"- {activity_date}"
        )

else:

    print(
        "No wellness activity recorded."
    )


# ---------------------------------------------------------
# Current Streak
# ---------------------------------------------------------

streak = get_wellness_streak(
    user.id
)

print("\nCurrent Wellness Streak:")

print(
    f"🔥 {streak} day(s)"
)


# ---------------------------------------------------------
# Activity Summary
# ---------------------------------------------------------

summary = get_wellness_activity_summary(
    user.id
)

print("\nWellness Activity Summary:")

print(
    f"Total active days: "
    f"{summary['total_active_days']}"
)

print(
    f"Active today: "
    f"{summary['active_today']}"
)

print(
    f"Current streak: "
    f"{summary['current_streak']} days"
)


print("\n" + "=" * 60)
print(
    "✅ Wellness service test completed."
)
print("=" * 60)