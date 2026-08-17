"""
AI memory services for MindEase.

Handles creating, retrieving, updating, and deleting
long-term AI memories for users.
"""

from sqlalchemy import select

from database.session import get_db
from models.ai_memory import AIMemory


# ---------------------------------------------------------
# Create Memory
# ---------------------------------------------------------

def create_memory(
    user_id: str,
    content: str,
    category: str = "general",
) -> AIMemory:
    """
    Create and save a new AI memory for a user.
    """

    content = content.strip()
    category = category.strip().lower()

    if not content:
        raise ValueError("Memory content cannot be empty.")

    if not category:
        category = "general"

    memory = AIMemory(
        user_id=user_id,
        category=category,
        content=content,
    )

    with get_db() as db:

        db.add(memory)

        db.commit()

        db.refresh(memory)

        return memory


# ---------------------------------------------------------
# Get All Memories
# ---------------------------------------------------------

def get_user_memories(
    user_id: str,
) -> list[AIMemory]:
    """
    Return all AI memories belonging to a user.

    Newest memories are returned first.
    """

    with get_db() as db:

        statement = (
            select(AIMemory)
            .where(
                AIMemory.user_id == user_id
            )
            .order_by(
                AIMemory.created_at.desc()
            )
        )

        return list(
            db.scalars(statement).all()
        )


# ---------------------------------------------------------
# Get Memories by Category
# ---------------------------------------------------------

def get_memories_by_category(
    user_id: str,
    category: str,
) -> list[AIMemory]:
    """
    Return memories belonging to a specific category.
    """

    category = category.strip().lower()

    with get_db() as db:

        statement = (
            select(AIMemory)
            .where(
                AIMemory.user_id == user_id,
                AIMemory.category == category,
            )
            .order_by(
                AIMemory.created_at.desc()
            )
        )

        return list(
            db.scalars(statement).all()
        )


# ---------------------------------------------------------
# Get Memory by ID
# ---------------------------------------------------------

def get_memory_by_id(
    memory_id: str,
    user_id: str,
) -> AIMemory | None:
    """
    Return a specific memory belonging to a user.
    """

    with get_db() as db:

        statement = (
            select(AIMemory)
            .where(
                AIMemory.id == memory_id,
                AIMemory.user_id == user_id,
            )
        )

        return db.scalar(statement)


# ---------------------------------------------------------
# Update Memory
# ---------------------------------------------------------

def update_memory(
    memory_id: str,
    user_id: str,
    content: str,
    category: str = "general",
) -> AIMemory | None:
    """
    Update an existing AI memory.

    Returns the updated memory or None if it does not exist.
    """

    content = content.strip()
    category = category.strip().lower()

    if not content:
        raise ValueError("Memory content cannot be empty.")

    if not category:
        category = "general"

    with get_db() as db:

        statement = (
            select(AIMemory)
            .where(
                AIMemory.id == memory_id,
                AIMemory.user_id == user_id,
            )
        )

        memory = db.scalar(statement)

        if memory is None:
            return None

        memory.content = content
        memory.category = category

        db.commit()

        db.refresh(memory)

        return memory


# ---------------------------------------------------------
# Delete Memory
# ---------------------------------------------------------

def delete_memory(
    memory_id: str,
    user_id: str,
) -> bool:
    """
    Delete a specific AI memory belonging to a user.

    Returns True if deleted, otherwise False.
    """

    with get_db() as db:

        statement = (
            select(AIMemory)
            .where(
                AIMemory.id == memory_id,
                AIMemory.user_id == user_id,
            )
        )

        memory = db.scalar(statement)

        if memory is None:
            return False

        db.delete(memory)

        db.commit()

        return True


# ---------------------------------------------------------
# Clear All Memories
# ---------------------------------------------------------

def clear_user_memories(
    user_id: str,
) -> int:
    """
    Delete all AI memories belonging to a user.

    Returns the number of deleted memories.
    """

    with get_db() as db:

        statement = (
            select(AIMemory)
            .where(
                AIMemory.user_id == user_id
            )
        )

        memories = list(
            db.scalars(statement).all()
        )

        for memory in memories:
            db.delete(memory)

        db.commit()

        return len(memories)