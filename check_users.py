from sqlalchemy import select

from database.session import get_db
from models.user import User

with get_db() as db:
    users = db.scalars(select(User)).all()

    print("=" * 50)

    if not users:
        print("No users found.")

    for user in users:
        print(user.id)
        print(user.full_name)
        print(user.email)
        print("-" * 30)