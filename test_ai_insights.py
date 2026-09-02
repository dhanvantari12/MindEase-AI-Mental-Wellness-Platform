from features.insights.services import (
    generate_ai_wellness_summary,
)

TEST_USER_ID = (
    "0dae12ad-a60b-4435-943e-da278f8180c8"
)

print(
    "\n============================================================"
)

print(
    "Testing MindEase AI Insights"
)

print(
    "============================================================\n"
)

summary = generate_ai_wellness_summary(
    TEST_USER_ID
)

print(summary)

print(
    "\n============================================================"
)

print(
    "✅ AI Insights Test Complete"
)

print(
    "============================================================"
)