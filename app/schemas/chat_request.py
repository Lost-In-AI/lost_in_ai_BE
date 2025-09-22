from pydantic import BaseModel, Field
from typing import Optional

from schemas.enums.bot_personality import BotPersonality
from schemas.message import Message
from uuid import UUID


class ChatRequest(BaseModel):
    session_id: Optional[UUID] = Field(
        ...,
        description="Unique identifier for the chat session"
    )
    current_message: str = Field(
        ...,
        description="The latest user message to be processed by the AI chatbot",
        max_length=1000
    )
    history: Optional[list[Message]] = Field(
        default=None,
        description="Optional list of the most recent N messages in the conversation"
    )
    summary: Optional[str] = Field(
        default=None,
        description="Optional condensed summary of the conversation, used to preserve context and reduce token usage"
    )
    bot_personality: Optional[BotPersonality] = Field(
        default=BotPersonality.WITTY,
        description="The bot's personality"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "session_id": "12345ABC",
                    "current_message": "La casa cost 100k ed è grande 100 metri quadri. Mi potete concedere il mutuo?"
                },
                {
                    "session_id": "12345ABC",
                    "current_message": "Ciao voglio informazioni per un mutuo",
                    "history": [
                        {
                            "sender": "user",
                            "text": "Ciao voglio informazioni per un mutuo",
                            "timestamp": "2025-09-05T15:02:00Z",
                        },
                        {
                            "sender": "bot",
                            "text": "L'agente umano è occupato al momento. Posso aiutarle con qualcosa di diverso?",
                            "timestamp": "2025-09-05T15:02:00Z",
                        },
                        {
                            "sender": "user",
                            "text": "Ciao voglio informazioni per un mutuo",
                            "currentMessage": "C'è un modo per essere messo in contatto con qualcuno?",
                            "summary": "L'utente ha chiesto di essere messo in contatto con qualcuno."
                        }
                    ],
                    "chat_personality": "witty"
                },
            ]
        }
    }
