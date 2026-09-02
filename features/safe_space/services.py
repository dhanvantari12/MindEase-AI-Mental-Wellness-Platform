"""
Safe Space services for MindEase.

Handles:
- Gemini AI responses
- Personalized AI companion names
- Long-term AI memory/context
- Conversation context
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

from features.ai.memory_extractor import (
    extract_memories_from_message
)


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
# Build Conversation Context
# ---------------------------------------------------------

def build_conversation_context(
    user_id: str,
    limit: int = 10,
) -> str:
    """
    Return the last few conversation messages
    as context for Gemini.
    """

    messages = get_conversation(user_id)

    if not messages:

        return "No previous conversation."

    recent_messages = messages[-limit:]

    lines = []

    for message in recent_messages:

        role = (
            "User"
            if message.role == "user"
            else "Assistant"
        )

        lines.append(
            f"{role}: {message.content}"
        )

    return "\n".join(lines)


# ---------------------------------------------------------
# Generate Gemini Response
# ---------------------------------------------------------

def generate_response(
    user_id: str,
    user_message: str,
    ai_name: str = "MindEase",
) -> str:
    """
    Generate a personalized AI response using Gemini.
    """

    try:

        # -------------------------------------------------
        # Long-term memory context
        # -------------------------------------------------

        ai_context = build_ai_context(
            user_id
        )

        # -------------------------------------------------
        # Recent conversation context
        # -------------------------------------------------

        conversation_context = (
            build_conversation_context(
                user_id=user_id,
                limit=10,
            )
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
RECENT CONVERSATION
--------------------------------------------------

{conversation_context}

--------------------------------------------------
AI COMPANION NAME
--------------------------------------------------

Your name for this user is:

{ai_name}

Always understand that when the user addresses you
as "{ai_name}", they are referring to you.

Use the name naturally when appropriate.

--------------------------------------------------
IMPORTANT MEMORY RULES
--------------------------------------------------

Use long-term memories only when relevant.

Use recent conversation history to maintain
continuity and avoid repeating questions.

Do not invent memories.

Do not reveal the memory system unless the user
asks what you remember.

--------------------------------------------------
CURRENT USER MESSAGE
--------------------------------------------------

{user_message}
"""

        # -------------------------------------------------
        # Gemini Request
        # -------------------------------------------------

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_message,
            config={
                "system_instruction": system_instruction,
            },
        )

        # -------------------------------------------------
        # Validate Response
        # -------------------------------------------------

        if response.text:

            return response.text.strip()

        return (
            "I'm here with you. "
            "Could you tell me a little more?"
        )

    except Exception as error:

        print(
            f"Gemini error: {error}"
        )

        return (
            "I'm sorry, but I'm having trouble "
            "responding right now. Please try again "
            "in a moment."
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
    Save a Safe Space conversation message.
    """
    if role == "user":

       try:

        extract_memories_from_message(
            user_id,
            content
        )

       except Exception as error:

        print(
            f"Memory extraction error: {error}"
        )
        
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
    Return all conversation messages.
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
    Delete all conversation messages.
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