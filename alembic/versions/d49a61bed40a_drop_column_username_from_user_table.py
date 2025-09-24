"""drop column username from user table

Revision ID: d49a61bed40a
Revises: 3e35c230f89f
Create Date: 2025-09-24 17:26:07.179229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd49a61bed40a'
down_revision: Union[str, Sequence[str], None] = '3e35c230f89f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("users", "username")


def downgrade() -> None:
    op.add_column("users", sa.Column("username", sa.String(50), nullable=False))
