from features.safe_space.services import generate_response


print("=" * 60)
print("Testing MindEase Safe Space")
print("=" * 60)

message = "I've had a stressful day and I'm feeling overwhelmed."

print("\nUser:")
print(message)

print("\nCalling Gemini...")

try:
    response = generate_response(message)

    print("\nMindEase response:")
    print(repr(response))

    print("\nNormal response:")
    print(response)

except Exception as e:
    print("\nERROR:")
    print(type(e).__name__)
    print(str(e))

print("\n" + "=" * 60)