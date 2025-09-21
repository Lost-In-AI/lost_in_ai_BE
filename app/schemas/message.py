from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from schemas.enums.bot_personality import BotPersonality
from schemas.enums.message_sender import MessageSender


class Message(BaseModel):
    sender: MessageSender = Field(
        ...,
        description="Indicates who sent the message ('user' or 'bot')"

    )
    bot_personality: Optional[BotPersonality] = Field(
        description="Indicates who sent the message ('user' or 'bot')",
        default=None
    )
    text: str = Field(
        ...,
        description="Message text",
    )
    timestamp: datetime = Field(
        ...,
        description="Timestamp"
    )
