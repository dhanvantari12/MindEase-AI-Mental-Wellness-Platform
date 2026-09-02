"""
Test MindEase Insights Services.
"""

from features.auth.services import login_user
from features.insights.services import get_user_insights


print("=" * 60)
print("Testing MindEase Insights Services")
print("=" * 60)


email = "reminder_test@mindease.com"
password = "TestPassword123!"


# ---------------------------------------------------------
# Login test user
# ---------------------------------------------------------

success, message, user = login_user(
    email=email,
    password=password,
)


if not success:

    print("❌ Login failed.")
    print(message)

    raise SystemExit


print()
print("User:")
print(user.full_name)
print(user.email)


# ---------------------------------------------------------
# Generate insights
# ---------------------------------------------------------

insights = get_user_insights(
    str(user.id)
)


print()
print("Mood Summary:")
print(
    insights["mood_summary"]
)


print()
print("Weekly Summary:")
print(
    insights["weekly_summary"]
)


print()
print("Journal Summary:")
print(
    insights["journal_summary"]
)


print()
print("Wellness Score:")
print(
    insights["wellness_score"]
)


print()
print("Generated Insights:")

for insight in insights["insights"]:

    print(
        f"- {insight}"
    )


print()
print("=" * 60)
print("✅ Insights service test completed.")
print("=" * 60)