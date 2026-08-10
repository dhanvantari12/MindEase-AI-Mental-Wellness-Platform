"""
Safe Space service for MindEase.

Handles:
- Gemini AI responses
- Saving conversation messages
- Retrieving conversation history
- Clearing conversation history
"""

import os

from dotenv import load_dotenv
from google import genai
from sqlalchemy import select

from database.session import get_db
from models.conversation import Conversation

load_dotenv()

# ---------------------------------------------------------
# Gemini Configuration
# ---------------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured."
    )

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ---------------------------------------------------------
# Safe Space System Instructions
# ---------------------------------------------------------

SYSTEM_INSTRUCTION = """
You are MindEase, a supportive AI mental wellness companion.

Your role is to:
- Listen empathetically.
- Respond in a calm and supportive manner.
- Encourage healthy reflection.
- Help users explore their feelings.
- Suggest practical and gentle coping strategies.
- Never judge, shame, or dismiss the user's feelings.

You are not a doctor, therapist, or emergency service.

Do not claim to diagnose mental health conditions.
Do not prescribe medication.
Do not present yourself as a replacement for professional care.

If a user appears to be in immediate danger or expresses
thoughts of self-harm or suicide, encourage them to contact
local emergency services or a qualified mental health
professional immediately.

Keep responses conversational, supportive, and reasonably concise.
"""


# ---------------------------------------------------------
# Generate Gemini Response
# ---------------------------------------------------------

def generate_response(
    user_message: str,
) -> str:
    """
    Generate a supportive response using Gemini.
    """

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_message,
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
            },
        )

        return response.text

    except Exception as error:

        print(
            f"Gemini error: {error}"
        )

        return (
            "I'm sorry, but I'm having trouble responding "
            "right now. Please try again in a moment."
        )


# ---------------------------------------------------------
# Save Conversation Message
# ---------------------------------------------------------

def save_message(
    user_id: str,
    role: str,
    content: str,
) -> Conversation:
    """
    Save a Safe Space conversation message
    to the database.
    """

    message = Conversation(
        user_id=user_id,
        role=role,
        content=content.strip(),
    )

    with get_db() as db:

        db.add(message)

        db.commit()

        db.refresh(message)

        return message


# ---------------------------------------------------------
# Get Conversation History
# ---------------------------------------------------------

def get_conversation(
    user_id: str,
) -> list[Conversation]:
    """
    Return all Safe Space messages for a user.

    Messages are returned from oldest
    to newest.
    """

    with get_db() as db:

        statement = (
            select(Conversation)
            .where(
                Conversation.user_id == user_id
            )
            .order_by(
                Conversation.created_at.asc()
            )
        )

        return list(
            db.scalars(statement).all()
        )


# ---------------------------------------------------------
# Clear Conversation
# ---------------------------------------------------------

def clear_conversation(
    user_id: str,
) -> None:
    """
    Delete all Safe Space messages
    belonging to a user.
    """

    with get_db() as db:

        statement = (
            select(Conversation)
            .where(
                Conversation.user_id == user_id
            )
        )

        messages = list(
            db.scalars(statement).all()
        )

        for message in messages:
            db.delete(message)

        db.commit()