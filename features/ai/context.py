"""
AI context builder for MindEase.

Combines relevant user information into a concise
context that can be provided to the AI assistant.
"""

from features.ai.memory import get_user_memories
from features.preferences.services import get_ai_name


# ---------------------------------------------------------
# Build Memory Context
# ---------------------------------------------------------

def build_memory_context(
    user_id: str,
) -> str:
    """
    Build a readable context string from the user's
    stored AI memories.
    """

    memories = get_user_memories(user_id)

    if not memories:
        return "No long-term memories are currently available."

    context_lines = []

    for memory in memories:

        context_lines.append(
            f"- [{memory.category}] {memory.content}"
        )

    return "\n".join(context_lines)


# ---------------------------------------------------------
# Build AI Context
# ---------------------------------------------------------

def build_ai_context(
    user_id: str,
) -> str:
    """
    Build the personalized context used by the AI.
    """

    ai_name = get_ai_name(user_id)

    if not ai_name:
        ai_name = "MindEase"

    memory_context = build_memory_context(
        user_id
    )

    context = f"""
USER AI ASSISTANT NAME:
{ai_name}

LONG-TERM USER MEMORIES:
{memory_context}
"""

    return context.strip()