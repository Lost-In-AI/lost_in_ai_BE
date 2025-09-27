"""add bot personality in message table

Revision ID: a6fc15ca0992
Revises: d49a61bed40a
Create Date: 2025-09-27 18:30:07.974667

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6fc15ca0992'
down_revision: Union[str, Sequence[str], None] = 'd49a61bed40a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("bot_personality", sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "bot_personality")