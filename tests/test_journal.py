from features.journal.services import (
    create_journal_entry,
    get_user_journal_entries,
    get_journal_entry_by_id,
    update_journal_entry,
    delete_journal_entry,
)


# Use an existing user ID from your database
USER_ID = "650efc4f-675f-48ca-b482-4865dd7baa81"


print("=" * 50)
print("Creating journal entry...")
print("=" * 50)

entry = create_journal_entry(
    user_id=USER_ID,
    title="My First Journal Entry",
    content="Today I started building the Journal module for MindEase.",
    mood="Good",
)

print("Created journal entry:")
print("ID:", entry.id)
print("Title:", entry.title)
print("Content:", entry.content)
print("Mood:", entry.mood)


print("\n" + "=" * 50)
print("Getting journal entries...")
print("=" * 50)

entries = get_user_journal_entries(USER_ID)

for journal_entry in entries:
    print(
        journal_entry.id,
        "|",
        journal_entry.title,
        "|",
        journal_entry.mood,
    )


print("\n" + "=" * 50)
print("Getting entry by ID...")
print("=" * 50)

found_entry = get_journal_entry_by_id(
    entry_id=entry.id,
    user_id=USER_ID,
)

if found_entry:
    print("Found:", found_entry.title)


print("\n" + "=" * 50)
print("Updating entry...")
print("=" * 50)

updated_entry = update_journal_entry(
    entry_id=entry.id,
    user_id=USER_ID,
    title="My Updated Journal Entry",
    content="I successfully created and connected the Journal module.",
    mood="Great",
)

if updated_entry:
    print("Updated title:", updated_entry.title)
    print("Updated mood:", updated_entry.mood)


print("\n" + "=" * 50)
print("Deleting entry...")
print("=" * 50)

deleted = delete_journal_entry(
    entry_id=entry.id,
    user_id=USER_ID,
)

print("Deleted:", deleted)

print("\nJournal service test completed successfully!")