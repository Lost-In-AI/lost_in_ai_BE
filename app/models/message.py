from datetime import datetime
from typing import Optional
from sqlalchemy import text
from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: int = Field(..., primary_key=True)
    session_id: str = Field(..., foreign_key="sessions.session_id")
    sender: str = Field(...)
    bot_personality: Optional[str] = Field(default=None)
    message: str = Field(...)
    created_at: Optional[datetime] = Field(
        ..., sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
