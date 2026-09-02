from features.ai.memory_extractor import (
    extract_memories_from_message
)

from features.ai.memory import (
    get_user_memories
)

TEST_USER = "memory-test-user"

extract_memories_from_message(
    TEST_USER,
    "I am preparing for product based company placements."
)

extract_memories_from_message(
    TEST_USER,
    "I am working on MindEase."
)

extract_memories_from_message(
    TEST_USER,
    "I like practical explanations."
)

memories = get_user_memories(
    TEST_USER
)

print("\nMEMORIES:\n")

for memory in memories:

    print(
        f"[{memory.category}] "
        f"{memory.content}"
    )