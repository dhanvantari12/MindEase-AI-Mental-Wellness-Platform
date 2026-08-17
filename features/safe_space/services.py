"""
Safe Space services for MindEase.

Handles:
- Gemini AI responses
- Personalized AI companion names
- Long-term AI memory/context
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

from features.ai.context import build_ai_context


# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Gemini Configuration
# ---------------------------------------------------------

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

if not GEMINI_API_KEY:

    raise ValueError(
        "GEMINI_API_KEY is not configured."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ---------------------------------------------------------
# Base Safe Space Instructions
# ---------------------------------------------------------

BASE_SYSTEM_INSTRUCTION = """
You are a supportive AI mental wellness companion
inside the MindEase application.

Your role is to:

- Listen empathetically.
- Respond in a calm and supportive manner.
- Encourage healthy reflection.
- Help users explore their feelings.
- Suggest practical and gentle coping strategies.
- Remember relevant information about the user when it
  is provided in the user context.
- Maintain a warm, respectful, and non-judgmental tone.
- Use the user's preferred AI companion name naturally.

You are not a doctor, therapist, or emergency service.

Do not:
- Diagnose mental health conditions.
- Prescribe medication.
- Claim to replace professional care.
- Make harmful or dangerous recommendations.
- Shame, judge, or dismiss the user's feelings.

If a user appears to be in immediate danger or expresses
thoughts of self-harm or suicide, encourage them to seek
immediate help from local emergency services or a qualified
mental health professional.

Keep responses conversational, supportive, personalized,
and reasonably concise.
"""


# ---------------------------------------------------------
# Generate Gemini Response
# ---------------------------------------------------------

def generate_response(
    user_message: str,
    user_id: str,
    ai_name: str = "MindEase",
) -> str:
    """
    Generate a personalized AI response using Gemini.

    The AI receives:
    - The user's current message
    - The personalized AI companion name
    - Long-term user memories
    """

    try:

        # -------------------------------------------------
        # Build personalized AI context
        # -------------------------------------------------

        ai_context = build_ai_context(
            user_id
        )

        # -------------------------------------------------
        # Personalized system instruction
        # -------------------------------------------------

        system_instruction = f"""
{BASE_SYSTEM_INSTRUCTION}

--------------------------------------------------
PERSONALIZED AI CONTEXT
--------------------------------------------------

{ai_context}

--------------------------------------------------
AI COMPANION NAME
--------------------------------------------------

Your name for this user is:

{ai_name}

Always understand that when the user addresses you
as "{ai_name}", they are referring to you.

Use the name naturally when appropriate.
Do not unnecessarily repeat your name in every response.

--------------------------------------------------
IMPORTANT MEMORY RULES
--------------------------------------------------

The long-term memories above are information about
the user that may help personalize your responses.

Use them only when relevant.

Do not reveal the memory system itself unless the
user explicitly asks about what you remember.

Do not invent memories.

If the context says there are no memories, simply
respond normally without mentioning that fact.

--------------------------------------------------
CURRENT USER MESSAGE
--------------------------------------------------

{user_message}
"""

        # -------------------------------------------------
        # Generate Gemini response
        # -------------------------------------------------

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_message,
            config={
                "system_instruction": system_instruction,
            },
        )

        # -------------------------------------------------
        # Validate response
        # -------------------------------------------------

        if response.text:

            return response.text.strip()

        return (
            f"I'm here with you. "
            f"Could you tell me a little more?"
        )

    except Exception as error:

        print(
            f"Gemini error: {error}"
        )

        return (
            f"I'm sorry, but I'm having trouble "
            f"responding right now. Please try again "
            f"in a moment."
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

            db.delete(
                message
            )

        db.commit()