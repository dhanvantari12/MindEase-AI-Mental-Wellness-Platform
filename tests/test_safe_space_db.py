from features.safe_space.services import (
    save_message,
    get_conversation,
    clear_conversation,
)


USER_ID = "650efc4f-675f-48ca-b482-4865dd7baa81"


print("=" * 60)
print("Testing Safe Space Database")
print("=" * 60)


# ---------------------------------------------------------
# Clear old test messages
# ---------------------------------------------------------

clear_conversation(USER_ID)

print("\nOld messages cleared.")


# ---------------------------------------------------------
# Save user message
# ---------------------------------------------------------

user_message = save_message(
    user_id=USER_ID,
    role="user",
    content="I've had a stressful day and I'm feeling overwhelmed.",
)

print("\nUser message saved:")
print(user_message.content)


# ---------------------------------------------------------
# Save assistant message
# ---------------------------------------------------------

assistant_message = save_message(
    user_id=USER_ID,
    role="assistant",
    content="I'm sorry you're having a difficult day. I'm here to listen.",
)

print("\nAssistant message saved:")
print(assistant_message.content)


# ---------------------------------------------------------
# Retrieve conversation
# ---------------------------------------------------------

messages = get_conversation(USER_ID)

print("\nConversation history:")

for message in messages:
    print(
        f"{message.role}: {message.content}"
    )


print("\n" + "=" * 60)
print("Safe Space database test completed successfully.")
print("=" * 60)