from pydantic import BaseModel, Field
from typing import Optional

from schemas.enums.bot_personality import BotPersonality
from schemas.enums.break_reason import BreakReason
from schemas.message import Message


class NewChatResponse(BaseModel):
    response_code: int = Field(
        ...,
        ge=100,
        lt=600,
        description="HTTP status code representing the result of the chat request"
    )
    session_id: str = Field(
        ...,
        description="Unique identifier for the chat session"
    )
    current_responses: list[Message] = Field(
        ...,
        description="The chatbot reply, split into multiple messages if the AI output contains pauses. "
                    "The frontend can insert musical interludes between parts."
    )
    history: Optional[list[Message]] = Field(
        default=None,
        description="Optional list of the most recent N messages in the conversation"
    )
    summary: Optional[str] = Field(
        default=None,
        description="Optional condensed summary of the conversation, used to preserve context and reduce token usage"
    )
    break_reason: Optional[BreakReason] = Field(
        default=None,
        description="Whether or not the conversation is currently playing"
    )
    message: Optional[str] = Field(
        default=None,
        description="Optional response message"
    )
    bot_personality: Optional[BotPersonality] = Field(
        default=BotPersonality.WITTY,
        description="The bot's personality"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "response_code": 200,
                    "session_id": "12345ABC",
                    "current_responses": [
                        {
                            "sender": "bot",
                            "text": "L'agente umano è occupato al momento. Posso aiutarle con qualcosa di diverso?",
                            "timestamp": "2025-09-05T15:02:00Z",
                        }
                    ],
                    "summary": "L'utente ha chiesto di essere messo in contatto con qualcuno.",
                    "history": [
                        {
                            "sender": "user",
                            "text": "Ciao voglio informazioni per un mutuo",
                            "timestamp": "2025-09-05T15:02:00Z",
                        },
                        {
                            "sender": "bot",
                            "text": "Ciao di quali info hai bisogno?",
                            "timestamp": "2025-09-05T15:03:00Z",
                        },
                        {
                            "sender": "user",
                            "text": "Voglio aprire un mutuo per acquistare una casa",
                            "timestamp": "2025-09-05T15:06:00Z",
                        },
                        {
                            "sender": "bot",
                            "text": "Puoi darmi altre info sulla casa? Come il prezzo di vendita, la metratura, lo "
                                    "stato energetico e soprattutto quanti soldi vuoi da noi!!",
                            "timestamp": "2025-09-05T15:07:00Z"
                        }
                    ],
                    "bot_personality": 'witty'
                }
            ]
        }
    }
