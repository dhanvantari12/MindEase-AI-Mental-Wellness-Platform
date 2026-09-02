"""
Weekly Wellness Report services.

Generates AI-powered wellness reports using:

- Mood history
- Journal activity
- Wellness score
- AI memories
"""

from features.insights.services import (
    get_user_insights,
)

from features.ai.memory import (
    get_user_memories,
)


# ---------------------------------------------------------
# Generate Weekly Wellness Report
# ---------------------------------------------------------

def generate_weekly_report(
    user_id: str,
) -> dict:
    """
    Generate a complete wellness report.
    """

    insights = get_user_insights(
        user_id
    )

    memories = get_user_memories(
        user_id
    )

    mood_summary = insights[
        "mood_summary"
    ]

    journal_summary = insights[
        "journal_summary"
    ]

    wellness_score = insights[
        "wellness_score"
    ]

    # -----------------------------------------------------
    # Memory Highlights
    # -----------------------------------------------------

    memory_highlights = []

    for memory in memories[:5]:

        memory_highlights.append(
            memory.content
        )

    # -----------------------------------------------------
    # Wellness Level
    # -----------------------------------------------------

    if wellness_score >= 80:

        wellness_level = (
            "Excellent"
        )

    elif wellness_score >= 60:

        wellness_level = (
            "Good"
        )

    elif wellness_score >= 40:

        wellness_level = (
            "Building Momentum"
        )

    else:

        wellness_level = (
            "Getting Started"
        )

    # -----------------------------------------------------
    # AI Summary
    # -----------------------------------------------------

    summary_lines = []

    summary_lines.append(
        f"You completed "
        f"{mood_summary['total_checkins']} "
        f"mood check-ins."
    )

    summary_lines.append(
        f"You wrote "
        f"{journal_summary['total_entries']} "
        f"journal entries."
    )

    if mood_summary[
        "most_common_mood"
    ]:

        summary_lines.append(
            f"Your most common mood was "
            f"{mood_summary['most_common_mood']}."
        )

    summary_lines.append(
        f"Current wellness score: "
        f"{wellness_score}/100."
    )

    ai_summary = " ".join(
        summary_lines
    )

    # -----------------------------------------------------
    # Recommendations
    # -----------------------------------------------------

    recommendations = []

    if (
        mood_summary["total_checkins"]
        < 5
    ):
        recommendations.append(
            "Try recording your mood daily."
        )

    if (
        journal_summary["total_entries"]
        < 3
    ):
        recommendations.append(
            "Write more journal reflections."
        )

    if wellness_score >= 70:

        recommendations.append(
            "Maintain your positive habits."
        )

    if not recommendations:

        recommendations.append(
            "Keep taking small wellness steps every day."
        )

    # -----------------------------------------------------
    # Final Report
    # -----------------------------------------------------

    return {
        "wellness_score":
            wellness_score,

        "wellness_level":
            wellness_level,

        "ai_summary":
            ai_summary,

        "memory_highlights":
            memory_highlights,

        "recommendations":
            recommendations,

        "mood_summary":
            mood_summary,

        "journal_summary":
            journal_summary,
    }