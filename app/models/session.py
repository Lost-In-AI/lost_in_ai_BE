from uuid import UUID
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel
from typing import Optional


class Session(SQLModel, table=True):
    __tablename__ = "sessions"

    id: int = Field(primary_key=True)
    session_id: UUID = Field(nullable=False, unique=True, index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
