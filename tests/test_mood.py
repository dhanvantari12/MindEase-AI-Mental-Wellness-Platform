from features.mood.services import (
    create_mood,
    get_latest_mood,
    get_user_moods,
)


USER_ID = "650efc4f-675f-48ca-b482-4865dd7baa81"


# Create a test mood
mood = create_mood(
    user_id=USER_ID,
    mood="Good",
    note="Testing the MindEase mood tracker.",
)

print("Created mood:")
print("ID:", mood.id)
print("Mood:", mood.mood)
print("Note:", mood.note)


# Get latest mood
latest = get_latest_mood(USER_ID)

print("\nLatest mood:")
print(latest.mood if latest else "None")


# Get all moods
moods = get_user_moods(USER_ID)

print("\nAll moods:")

for item in moods:
    print(
        item.mood,
        "|",
        item.note,
        "|",
        item.created_at,
    )