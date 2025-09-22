"""create_sessions_table

Revision ID: 441df839693d
Revises: e65f82af81bc
Create Date: 2025-09-22 18:56:47.657474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '441df839693d'
down_revision: Union[str, Sequence[str], None] = 'e65f82af81bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_sessions_user_id_users", ondelete="CASCADE"),
        sa.UniqueConstraint("session_id", "user_id", name="uq_sessions_session_id_user_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("sessions")