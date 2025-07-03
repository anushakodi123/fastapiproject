"""add foreign-key to posts table

Revision ID: 9de2183f485b
Revises: de23f186c9bf
Create Date: 2025-07-03 12:25:54.438153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9de2183f485b'
down_revision: Union[str, Sequence[str], None] = 'de23f186c9bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                          local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'user_id')
    pass
