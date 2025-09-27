"""add column user_id in user table

Revision ID: 3e35c230f89f
Revises: e8e618d2010f
Create Date: 2025-09-24 15:06:13.128689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e35c230f89f'
down_revision: Union[str, Sequence[str], None] = 'e8e618d2010f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("user_id", sa.String(255), nullable=False, unique=True))


def downgrade() -> None:
    op.drop_column("users", "user_id")

