"""remove birthdate from users

Revision ID: e8e618d2010f
Revises: 1e64e34129e0
Create Date: 2025-09-23 19:37:55.831908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8e618d2010f'
down_revision: Union[str, Sequence[str], None] = '1e64e34129e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("users", "date_of_birth")


def downgrade() -> None:
    op.add_column("users", sa.Column("date_of_birth", sa.DATE(), nullable=False))
