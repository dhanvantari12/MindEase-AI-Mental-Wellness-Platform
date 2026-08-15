"""
Test user preferences services.
"""

from features.auth.services import (
    get_user_by_email,
)

from features.preferences.services import (
    get_or_create_preferences,
    update_preferences,
)


print("=" * 60)
print("Testing MindEase User Preferences Services")
print("=" * 60)


# ---------------------------------------------------------
# Find existing test user
# ---------------------------------------------------------

email = "reminder_test@mindease.com"

user = get_user_by_email(
    email
)

if user is None:

    print(
        f"❌ Test user not found: {email}"
    )

    print(
        "Please login/register this user first."
    )

    raise SystemExit(1)


print()
print("User:")
print(user.full_name)
print(user.email)


user_id = user.id


# ---------------------------------------------------------
# Get or create preferences
# ---------------------------------------------------------

preferences = get_or_create_preferences(
    user_id
)


print()
print("Default Preferences:")
print(
    "Reminders:",
    preferences.reminders_enabled,
)

print(
    "Daily Check-in:",
    preferences.daily_checkin_enabled,
)

print(
    "Journal Prompts:",
    preferences.journal_prompts_enabled,
)


# ---------------------------------------------------------
# Update preferences
# ---------------------------------------------------------

updated_preferences = update_preferences(
    user_id=user_id,
    reminders_enabled=False,
    daily_checkin_enabled=True,
    journal_prompts_enabled=False,
)


print()
print("Updated Preferences:")
print(
    "Reminders:",
    updated_preferences.reminders_enabled,
)

print(
    "Daily Check-in:",
    updated_preferences.daily_checkin_enabled,
)

print(
    "Journal Prompts:",
    updated_preferences.journal_prompts_enabled,
)


# ---------------------------------------------------------
# Verify persistence
# ---------------------------------------------------------

saved_preferences = get_or_create_preferences(
    user_id
)


print()
print("Reloaded Preferences:")
print(
    "Reminders:",
    saved_preferences.reminders_enabled,
)

print(
    "Daily Check-in:",
    saved_preferences.daily_checkin_enabled,
)

print(
    "Journal Prompts:",
    saved_preferences.journal_prompts_enabled,
)


print()
print("=" * 60)
print("✅ Preferences service test completed.")
print("=" * 60)