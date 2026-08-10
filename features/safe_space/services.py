"""
AI service for MindEase Safe Space.

Handles communication with the Gemini API.
"""

import os

from dotenv import load_dotenv
from google import genai


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Gemini configuration
# ---------------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to your .env file."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ---------------------------------------------------------
# System instructions
# ---------------------------------------------------------

SYSTEM_INSTRUCTION = """
You are MindEase, a supportive AI wellness companion.

Your role is to:
- Listen without judgment.
- Respond with empathy and warmth.
- Encourage healthy reflection.
- Help users explore their feelings.
- Offer practical, gentle suggestions when appropriate.
- Never claim to be a human therapist or doctor.
- Never diagnose mental health conditions.
- Never encourage harmful behavior.

Keep responses conversational and reasonably concise.

If a user appears to be in immediate danger or expresses
intent to seriously hurt themselves or someone else,
prioritize immediate safety and encourage them to contact
local emergency services or a trusted person who can help
them right now.
"""


# ---------------------------------------------------------
# Generate AI response
# ---------------------------------------------------------

def generate_response(
    user_message: str,
) -> str:
    """
    Generate a response from Gemini.

    Parameters
    ----------
    user_message:
        Message written by the user.

    Returns
    -------
    str
        Gemini's response.
    """

    if not user_message.strip():
        return "Please write something first."

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_message,
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
            },
        )

        if response.text:
            return response.text

        return (
            "I'm sorry, I couldn't generate a response "
            "right now. Please try again."
        )

    except Exception as e:
        print("Gemini error:", type(e).__name__, str(e))
        raise