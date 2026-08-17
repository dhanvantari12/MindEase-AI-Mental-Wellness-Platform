"""
Test AI context builder for MindEase.
"""

from features.ai.context import (
    build_memory_context,
    build_ai_context,
)


TEST_USER_ID = "704f4b24-fc91-4d11-b072-b4296d2a8abe"


print("=" * 60)
print("Testing MindEase AI Context Builder")
print("=" * 60)


print()
print("Memory Context:")
print("-" * 60)

memory_context = build_memory_context(
    TEST_USER_ID
)

print(memory_context)


print()
print("Full AI Context:")
print("-" * 60)

ai_context = build_ai_context(
    TEST_USER_ID
)

print(ai_context)


print()
print("=" * 60)
print("✅ AI context test completed.")
print("=" * 60)