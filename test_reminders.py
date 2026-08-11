"""
Tests for MindEase reminder services.
"""

from datetime import datetime, timedelta

from features.auth.services import login_user

from features.reminders.services import (
    create_reminder,
    get_user_reminders,
    get_pending_reminders,
    get_completed_reminders,
    mark_reminder_completed,
    mark_reminder_pending,
    update_reminder,
    delete_reminder,
)


print("=" * 60)
print("Testing MindEase Reminder Services")
print("=" * 60)


# ---------------------------------------------------------
# Login existing test user
# ---------------------------------------------------------

email = "reminder_test@mindease.com"
password = "TestPassword123!"

success, message, user = login_user(
    email=email,
    password=password,
)

if not success or user is None:

    print()
    print("ERROR: Could not login test user.")
    print("Message:", message)
    print()
    print(
        "Create this test user through the MindEase "
        "Sign Up page first:"
    )
    print()
    print("Name:     Reminder Test User")
    print("Email:    reminder_test@mindease.com")
    print("Password: TestPassword123!")
    print()
    raise SystemExit


user_id = str(user.id)

print()
print("Test user:")
print(user.full_name)
print(user.email)


# ---------------------------------------------------------
# Create reminder
# ---------------------------------------------------------

reminder_time = datetime.now() + timedelta(
    hours=1
)

reminder = create_reminder(
    user_id=user_id,
    title="Take a short break",
    description="Step away from the screen and relax.",
    reminder_time=reminder_time,
)

print()
print("Reminder created:")
print("Title:", reminder.title)
print("Time:", reminder.reminder_time)


# ---------------------------------------------------------
# Get all reminders
# ---------------------------------------------------------

reminders = get_user_reminders(
    user_id
)

print()
print(
    "Total reminders:",
    len(reminders)
)


# ---------------------------------------------------------
# Get pending reminders
# ---------------------------------------------------------

pending = get_pending_reminders(
    user_id
)

print(
    "Pending reminders:",
    len(pending)
)


# ---------------------------------------------------------
# Mark completed
# ---------------------------------------------------------

completed = mark_reminder_completed(
    reminder_id=str(reminder.id),
    user_id=user_id,
)

print()
print(
    "Marked completed:",
    completed
)


# ---------------------------------------------------------
# Verify completed
# ---------------------------------------------------------

completed_reminders = get_completed_reminders(
    user_id
)

print(
    "Completed reminders:",
    len(completed_reminders)
)


# ---------------------------------------------------------
# Mark pending again
# ---------------------------------------------------------

pending_again = mark_reminder_pending(
    reminder_id=str(reminder.id),
    user_id=user_id,
)

print()
print(
    "Marked pending again:",
    pending_again
)


# ---------------------------------------------------------
# Update reminder
# ---------------------------------------------------------

updated = update_reminder(
    reminder_id=str(reminder.id),
    user_id=user_id,
    title="Take a relaxing break",
    description=(
        "Drink some water and take a few "
        "deep breaths."
    ),
    reminder_time=datetime.now()
    + timedelta(hours=2),
)

print()
print(
    "Updated reminder:",
    updated.title if updated else None
)


# ---------------------------------------------------------
# Delete reminder
# ---------------------------------------------------------

deleted = delete_reminder(
    reminder_id=str(reminder.id),
    user_id=user_id,
)

print()
print(
    "Reminder deleted:",
    deleted
)


# ---------------------------------------------------------
# Final verification
# ---------------------------------------------------------

remaining = get_user_reminders(
    user_id
)

print(
    "Remaining reminders:",
    len(remaining)
)

print()
print("=" * 60)
print("Reminder service test completed successfully.")
print("=" * 60)