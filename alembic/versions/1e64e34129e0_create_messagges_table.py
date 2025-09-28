"""create_messagges_table

Revision ID: 1e64e34129e0
Revises: 441df839693d
Create Date: 2025-09-22 18:57:03.248740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '1e64e34129e0'
down_revision: Union[str, Sequence[str], None] = '441df839693d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    bind = op.get_bind()

    msg_sender_enum = postgresql.ENUM(
        'user', 'assistant', 'system',
        name='message_sender_enum',
        create_type=False,
    )
    msg_sender_enum.create(bind, checkfirst=True)

    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('session_id', sa.String, nullable=False),
        sa.Column('sender', msg_sender_enum, nullable=False),
        sa.Column('message', sa.Text, nullable=False),
        sa.ForeignKeyConstraint(
            ['session_id'], ['sessions.session_id'],
            name='fk_messages_session_id_sessions', ondelete='CASCADE'
        ),
    )


def downgrade():
    op.drop_table('messages')

    bind = op.get_bind()
    msg_sender_enum = postgresql.ENUM(
        'user', 'assistant', 'system',
        name='message_sender_enum',
        create_type=False,
    )
    msg_sender_enum.drop(bind, checkfirst=True)
