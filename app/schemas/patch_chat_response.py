from pydantic import BaseModel, Field
from typing import Optional

from schemas.enums.bot_personality import BotPersonality


class PatchChatResponse(BaseModel):
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
                    "bot_personality": 'witty'
                }
            ]
        }
    }
