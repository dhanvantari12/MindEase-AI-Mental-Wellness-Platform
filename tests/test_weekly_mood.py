from features.mood.services import get_weekly_mood_counts


# Use the ID of one of your test users.
user_id = "650efc4f-675f-48ca-b482-4865dd7baa81"


counts = get_weekly_mood_counts(user_id)


print("=" * 40)
print("Weekly Mood Counts")
print("=" * 40)

for mood, count in counts.items():
    print(f"{mood}: {count}")