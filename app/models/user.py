from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import UniqueConstraint, text
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
        UniqueConstraint("email", name="uq_users_email"),
    )

    id: int = Field(..., primary_key=True)
    username: str = Field(...)
    email: str = Field(...)
    name: str = Field(...)
    surname: str = Field(...)
    created_at: Optional[datetime] = Field(
        ..., sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
