"""create base tables

Revision ID: 4f902f4e8380
Revises: 
Create Date: 2025-09-22 16:31:22.922060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "4f902f4e8380"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

message_sender_enum = postgresql.ENUM("user", "assistant", "system", name="message_sender")

def upgrade() -> None:
    bind = op.get_bind()
    message_sender_enum.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("email", sa.String(100), nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("surname", sa.String(50), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=False), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("username", name="uq_users_username"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_sessions_user_id_users", ondelete="CASCADE"),
        sa.UniqueConstraint("session_id", "user_id", name="uq_sessions_session_id_user_id"),
    )

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("sender", postgresql.ENUM(name="message_sender", create_type=False), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=False), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"], name="fk_messages_session_id_sessions", ondelete="CASCADE"),
    )

def downgrade() -> None:
    op.drop_table("messages")
    op.drop_table("sessions")
    op.drop_table("users")
    bind = op.get_bind()
    message_sender_enum.drop(bind, checkfirst=True)