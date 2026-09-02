"""
Test AI memory services for MindEase.
"""

from features.ai.memory import (
    create_memory,
    get_user_memories,
    get_memories_by_category,
    update_memory,
    delete_memory,
    clear_user_memories,
)


TEST_USER_ID = "704f4b24-fc91-4d11-b072-b4296d2a8abe"


print("=" * 60)
print("Testing MindEase AI Memory Services")
print("=" * 60)


# ---------------------------------------------------------
# Clear old test memories
# ---------------------------------------------------------

deleted = clear_user_memories(TEST_USER_ID)

print()
print(f"Cleared old memories: {deleted}")


# ---------------------------------------------------------
# Create memories
# ---------------------------------------------------------

memory1 = create_memory(
    user_id=TEST_USER_ID,
    category="goal",
    content="Preparing for a software engineering interview.",
)

memory2 = create_memory(
    user_id=TEST_USER_ID,
    category="preference",
    content="Prefers concise and practical explanations.",
)

memory3 = create_memory(
    user_id=TEST_USER_ID,
    category="study",
    content="Currently working on a college project.",
)


print()
print("Created memories:")
print(f"- {memory1.category}: {memory1.content}")
print(f"- {memory2.category}: {memory2.content}")
print(f"- {memory3.category}: {memory3.content}")


# ---------------------------------------------------------
# Get all memories
# ---------------------------------------------------------

memories = get_user_memories(TEST_USER_ID)

print()
print(f"Total memories: {len(memories)}")

for memory in memories:
    print(
        f"- [{memory.category}] "
        f"{memory.content}"
    )


# ---------------------------------------------------------
# Get category memories
# ---------------------------------------------------------

goal_memories = get_memories_by_category(
    TEST_USER_ID,
    "goal",
)

print()
print("Goal memories:")

for memory in goal_memories:
    print(
        f"- {memory.content}"
    )


# ---------------------------------------------------------
# Update memory
# ---------------------------------------------------------

updated = update_memory(
    memory_id=memory1.id,
    user_id=TEST_USER_ID,
    category="goal",
    content="Preparing for a product-based company software engineering interview.",
)

print()
print("Updated memory:")

if updated:
    print(
        f"- [{updated.category}] "
        f"{updated.content}"
    )


# ---------------------------------------------------------
# Delete memory
# ---------------------------------------------------------

deleted_successfully = delete_memory(
    memory_id=memory2.id,
    user_id=TEST_USER_ID,
)

print()
print(
    f"Memory deleted: {deleted_successfully}"
)


# ---------------------------------------------------------
# Final memories
# ---------------------------------------------------------

final_memories = get_user_memories(
    TEST_USER_ID
)

print()
print(
    f"Final memory count: "
    f"{len(final_memories)}"
)

print()
print("=" * 60)
print("✅ AI memory service test completed.")
print("=" * 60)