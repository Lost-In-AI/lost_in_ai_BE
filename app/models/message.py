from datetime import datetime
from typing import Optional
from sqlalchemy import text
from sqlmodel import Field, SQLModel

from schemas.enums.message_sender import MessageSender


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: int = Field(..., primary_key=True)
    session_id: int = Field(..., foreign_key="sessions.id")
    sender: MessageSender = Field(...)
    message: str = Field(...)
    created_at: Optional[datetime] = Field(
        ..., sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
