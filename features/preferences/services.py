"""
User preferences services for MindEase.

Handles creating, retrieving, and updating
application preferences for users.
"""

from sqlalchemy import select

from database.session import get_db
from models.user_preferences import UserPreferences


# ---------------------------------------------------------
# Get User Preferences
# ---------------------------------------------------------

def get_user_preferences(
    user_id: str,
) -> UserPreferences | None:
    """
    Return the preferences belonging to a user.

    Returns None if preferences have not been created yet.
    """

    with get_db() as db:

        statement = (
            select(UserPreferences)
            .where(
                UserPreferences.user_id == user_id
            )
        )

        return db.scalar(statement)


# ---------------------------------------------------------
# Create Default Preferences
# ---------------------------------------------------------

def create_default_preferences(
    user_id: str,
) -> UserPreferences:
    """
    Create default preferences for a user.
    """

    preferences = UserPreferences(
        user_id=user_id,
        ai_name="MindEase",
        reminders_enabled=True,
        daily_checkin_enabled=True,
        journal_prompts_enabled=True,
    )

    with get_db() as db:

        db.add(preferences)

        db.commit()

        db.refresh(preferences)

        return preferences


# ---------------------------------------------------------
# Get Or Create Preferences
# ---------------------------------------------------------

def get_or_create_preferences(
    user_id: str,
) -> UserPreferences:
    """
    Return existing preferences.

    If the user does not have preferences yet,
    create them with default values.
    """

    preferences = get_user_preferences(
        user_id
    )

    if preferences is not None:
        return preferences

    return create_default_preferences(
        user_id
    )


# ---------------------------------------------------------
# Get AI Name
# ---------------------------------------------------------

def get_ai_name(
    user_id: str,
) -> str:
    """
    Return the user's selected AI companion name.

    If preferences do not exist, default preferences
    are created automatically.
    """

    preferences = get_or_create_preferences(
        user_id
    )

    return (
        preferences.ai_name.strip()
        if preferences.ai_name
        else "MindEase"
    )


# ---------------------------------------------------------
# Update AI Name
# ---------------------------------------------------------

def update_ai_name(
    user_id: str,
    ai_name: str,
) -> UserPreferences:
    """
    Update the user's AI companion name.

    Empty names are replaced with the default
    name 'MindEase'.
    """

    ai_name = ai_name.strip()

    if not ai_name:
        ai_name = "MindEase"

    # Keep the name within the database limit.
    ai_name = ai_name[:50]

    with get_db() as db:

        statement = (
            select(UserPreferences)
            .where(
                UserPreferences.user_id == user_id
            )
        )

        preferences = db.scalar(statement)

        # -------------------------------------------------
        # Create preferences if missing
        # -------------------------------------------------

        if preferences is None:

            preferences = UserPreferences(
                user_id=user_id,
                ai_name=ai_name,
                reminders_enabled=True,
                daily_checkin_enabled=True,
                journal_prompts_enabled=True,
            )

            db.add(preferences)

        # -------------------------------------------------
        # Update existing preferences
        # -------------------------------------------------

        else:

            preferences.ai_name = ai_name

        db.commit()

        db.refresh(preferences)

        return preferences


# ---------------------------------------------------------
# Update All Preferences
# ---------------------------------------------------------

def update_preferences(
    user_id: str,
    reminders_enabled: bool,
    daily_checkin_enabled: bool,
    journal_prompts_enabled: bool,
) -> UserPreferences:
    """
    Update the user's application preferences.

    If preferences do not exist, they are created first.

    Note:
    The AI companion name is handled separately through
    update_ai_name().
    """

    with get_db() as db:

        statement = (
            select(UserPreferences)
            .where(
                UserPreferences.user_id == user_id
            )
        )

        preferences = db.scalar(statement)

        # -------------------------------------------------
        # Create preferences if missing
        # -------------------------------------------------

        if preferences is None:

            preferences = UserPreferences(
                user_id=user_id,
                ai_name="MindEase",
                reminders_enabled=reminders_enabled,
                daily_checkin_enabled=(
                    daily_checkin_enabled
                ),
                journal_prompts_enabled=(
                    journal_prompts_enabled
                ),
            )

            db.add(preferences)

        # -------------------------------------------------
        # Update existing preferences
        # -------------------------------------------------

        else:

            preferences.reminders_enabled = (
                reminders_enabled
            )

            preferences.daily_checkin_enabled = (
                daily_checkin_enabled
            )

            preferences.journal_prompts_enabled = (
                journal_prompts_enabled
            )

        db.commit()

        db.refresh(preferences)

        return preferences