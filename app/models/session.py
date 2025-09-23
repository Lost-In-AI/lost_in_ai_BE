from __future__ import annotations

from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class Session(SQLModel, table=True):
    __tablename__ = "sessions"
    __table_args__ = (
        UniqueConstraint(
            "session_id", "user_id", name="uq_sessions_session_id_user_id"
        ),
    )

    id: int = Field(..., primary_key=True)
    session_id: UUID = Field(..., unique=True)
    user_id: int = Field(..., foreign_key="users.id")
