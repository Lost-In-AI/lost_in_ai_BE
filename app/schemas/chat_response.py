from pydantic import BaseModel, Field
from typing import Optional

from schemas.enums.break_reason import BreakReason
from schemas.message import Message


class ChatResponse(BaseModel):
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


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "response_code": 200,
                    "session_id": "b8962d03-ef87-452a-b54f-08d1f5c686a4",
                    "current_responses": [
                        {
                            "sender": "bot",
                            "text": "L'agente umano è occupato al momento. Posso aiutarle con qualcosa di diverso?",
                            "timestamp": "2025-09-05T15:02:00Z",
                        }
                    ],
                    "summary": "L'utente ha chiesto di essere messo in contatto con qualcuno.",
                }
            ]
        }
    }
