from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from schemas.enums.bot_personality import BotPersonality


class ChatRequest(BaseModel):
    session_id: Optional[UUID] = Field(
        description="Unique identifier for the chat session",
        default=None
    )
    current_message: str = Field(
        ...,
        description="The latest user message to be processed by the AI chatbot",
        max_length=1000
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
                    "session_id": "b8962d03-ef87-452a-b54f-08d1f5c686a4",
                    "current_message": "La casa cost 100k ed è grande 100 metri quadri. Mi potete concedere il mutuo?"
                },
                {
                    "session_id": "b8962d03-ef87-452a-b54f-08d1f5c686a4",
                    "current_message": "Ciao voglio informazioni per un mutuo",
                    "chat_personality": "witty"
                },
            ]
        }
    }
