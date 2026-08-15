"""
Safe Space service for MindEase.

Handles:
- Gemini AI responses
- Personalized AI companion name
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


# ---------------------------------------------------------
# Environment Configuration
# ---------------------------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured."
    )


# ---------------------------------------------------------
# Gemini Client
# ---------------------------------------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ---------------------------------------------------------
# Default AI Name
# ---------------------------------------------------------

DEFAULT_AI_NAME = "MindEase"


# ---------------------------------------------------------
# Safe Space System Instructions
# ---------------------------------------------------------

def build_system_instruction(
    ai_name: str,
) -> str:
    """
    Build the system instruction for the AI companion.

    The AI receives a personalized name chosen
    by the user.
    """

    ai_name = (
        ai_name.strip()
        if ai_name
        else DEFAULT_AI_NAME
    )

    return f"""
You are {ai_name}, a supportive AI mental wellness
companion inside the MindEase application.

Your name is {ai_name}.

PERSONALITY:
- Calm
- Warm
- Empathetic
- Patient
- Non-judgmental
- Respectful
- Encouraging
- Conversational

YOUR ROLE:

Your role is to:
- Listen carefully to what the user says.
- Respond with empathy and understanding.
- Help the user reflect on their thoughts and feelings.
- Encourage healthy emotional awareness.
- Suggest practical, gentle coping strategies when appropriate.
- Ask thoughtful follow-up questions when they would help.
- Celebrate small positive steps.
- Avoid making the user feel judged, blamed, or dismissed.

CONVERSATION STYLE:

- Talk naturally, like a supportive companion.
- Do not sound robotic or overly formal.
- Keep responses reasonably concise.
- Do not give long lectures unless the user asks for
  detailed information.
- Match the emotional tone of the user.
- If the user is sad, respond gently.
- If the user is excited, respond positively.
- If the user is confused, explain things clearly.
- If the user simply wants someone to listen, listen first
  instead of immediately giving advice.

PERSONALIZATION:

The user has chosen the name "{ai_name}" for you.

Use this identity naturally when appropriate.

Do not repeatedly introduce yourself as {ai_name}.
Do not force your name into every response.

IMPORTANT LIMITATIONS:

You are an AI wellness companion.

You are NOT:
- A doctor
- A psychologist
- A psychiatrist
- A therapist
- An emergency service

Never claim to diagnose a mental health condition.

Never prescribe medication.

Never tell the user to stop or change prescribed
medication.

Never present yourself as a replacement for qualified
professional care.

SAFETY:

If the user expresses thoughts of self-harm, suicide,
or appears to be in immediate danger:

- Respond with empathy.
- Encourage them to seek immediate support from a
  trusted person or qualified professional.
- Encourage contacting appropriate local emergency
  services when there is immediate danger.
- Do not provide instructions, methods, or encouragement
  for self-harm.

Do not shame or frighten the user.

GENERAL RULE:

Your goal is to make the user feel heard, respected,
and supported while maintaining appropriate boundaries
as an AI wellness companion.
"""


# ---------------------------------------------------------
# Conversation Context
# ---------------------------------------------------------

def get_conversation_context(
    user_id: str,
    limit: int = 12,
) -> list[dict[str, str]]:
    """
    Retrieve recent conversation messages for AI context.

    Only the most recent messages are included to prevent
    the prompt from growing indefinitely.
    """

    messages = get_conversation(
        user_id=user_id
    )

    recent_messages = messages[-limit:]

    context = []

    for message in recent_messages:

        role = message.role

        # Gemini accepts user/model style roles.
        if role == "assistant":
            role = "model"

        context.append(
            {
                "role": role,
                "text": message.content,
            }
        )

    return context


# ---------------------------------------------------------
# Generate Gemini Response
# ---------------------------------------------------------

def generate_response(
    user_message: str,
    ai_name: str = DEFAULT_AI_NAME,
    user_id: str | None = None,
) -> str:
    """
    Generate a personalized supportive response using Gemini.

    Parameters:
    user_message:
        The latest message from the user.

    ai_name:
        The personalized name selected by the user.

    user_id:
        Optional user ID used to load recent conversation
        history for contextual responses.
    """

    try:

        # -------------------------------------------------
        # Normalize AI name
        # -------------------------------------------------

        ai_name = (
            ai_name.strip()
            if ai_name
            else DEFAULT_AI_NAME
        )

        # -------------------------------------------------
        # Build system instruction
        # -------------------------------------------------

        system_instruction = build_system_instruction(
            ai_name
        )

        # -------------------------------------------------
        # Build conversation contents
        # -------------------------------------------------

        contents = []

        if user_id:

            conversation_context = (
                get_conversation_context(
                    user_id=user_id,
                    limit=12,
                )
            )

            for message in conversation_context:

                contents.append(
                    {
                        "role": message["role"],
                        "parts": [
                            {
                                "text": message["text"]
                            }
                        ],
                    }
                )

        # -------------------------------------------------
        # Add latest user message
        # -------------------------------------------------

        contents.append(
            {
                "role": "user",
                "parts": [
                    {
                        "text": user_message.strip()
                    }
                ],
            }
        )

        # -------------------------------------------------
        # Generate response
        # -------------------------------------------------

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
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
            "I'm here with you. Could you tell me a little "
            "more about what's on your mind?"
        )

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