from features.auth.session_service import (
    create_session,
    get_user_from_session,
    delete_session,
)

from database.session import get_db
from models.user import User


print("=" * 60)
print("Testing Persistent Login Session")
print("=" * 60)


# ---------------------------------------------------------
# Get a test user
# ---------------------------------------------------------

with get_db() as db:

    user = db.query(User).first()


if user is None:

    print("No user found in database.")
    print("Create an account first.")

    raise SystemExit


print("\nUser:")
print(user.full_name)
print(user.email)


# ---------------------------------------------------------
# Create session
# ---------------------------------------------------------

token = create_session(
    user_id=user.id
)

print("\nSession created.")
print("Token generated:", bool(token))


# ---------------------------------------------------------
# Validate session
# ---------------------------------------------------------

restored_user = get_user_from_session(
    token
)

print("\nRestored user:")

if restored_user:

    print(
        restored_user.full_name
    )

    print(
        restored_user.email
    )

else:

    print("FAILED")


# ---------------------------------------------------------
# Delete session
# ---------------------------------------------------------

delete_session(token)

print("\nSession deleted.")


# ---------------------------------------------------------
# Verify deletion
# ---------------------------------------------------------

restored_user = get_user_from_session(
    token
)

if restored_user is None:

    print(
        "Session deletion verified."
    )

else:

    print(
        "ERROR: Session still exists."
    )


print("\n" + "=" * 60)
print("Persistent session test completed.")
print("=" * 60)