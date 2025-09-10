from pydantic import BaseModel, Field
from datetime import datetime
from models.enums.message_sender import MessageSender


class Message(BaseModel):
    sender: MessageSender = Field(
        ...,
        description="Indicates who sent the message ('user' or 'bot')"

    )
    text: str = Field(
        ...,
        description="Message text",
    )
    timestamp: datetime = Field(
        ...,
        description="Timestamp"

    )
