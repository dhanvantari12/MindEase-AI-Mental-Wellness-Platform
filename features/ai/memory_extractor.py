# features/ai/memory_extractor.py

"""
Automatic memory extraction for MindEase.

Analyzes user messages and stores useful
long-term memories automatically.
"""

import re

from features.ai.memory import (
    create_memory,
    get_user_memories,
)


# ---------------------------------------------------------
# Memory Patterns
# ---------------------------------------------------------

MEMORY_PATTERNS = [

    (
        "goal",
        [
            r"i want to become (.+)",
            r"i want to be (.+)",
            r"my goal is (.+)",
            r"i am preparing for (.+)",
        ]
    ),

    (
        "project",
        [
            r"i am working on (.+)",
            r"currently building (.+)",
            r"my project is (.+)",
        ]
    ),

    (
        "preference",
        [
            r"i like (.+)",
            r"my favorite (.+)",
            r"i prefer (.+)",
        ]
    ),

    (
        "education",
        [
            r"i study at (.+)",
            r"i am studying at (.+)",
            r"i am a student of (.+)",
        ]
    ),
]

# ---------------------------------------------------------
# Extract Memories
# ---------------------------------------------------------

def extract_memories_from_message(
    user_id: str,
    message: str,
) -> int:

    message_lower = message.lower()

    created_count = 0

    existing_memories = get_user_memories(
        user_id
    )

    existing_texts = {
        memory.content.lower()
        for memory in existing_memories
    }

    for category, patterns in MEMORY_PATTERNS:

        for pattern in patterns:

            match = re.search(
                pattern,
                message_lower
            )

            if not match:
                continue

            memory_content = (
                match.group(1)
                .strip()
                .capitalize()
            )

            if (
                memory_content.lower()
                in existing_texts
            ):
                continue

            create_memory(
                user_id=user_id,
                category=category,
                content=memory_content,
            )

            created_count += 1

    return created_count