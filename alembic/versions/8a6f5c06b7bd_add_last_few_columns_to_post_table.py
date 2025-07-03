"""add last few columns to post table

Revision ID: 8a6f5c06b7bd
Revises: 9de2183f485b
Create Date: 2025-07-03 14:44:43.061025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a6f5c06b7bd'
down_revision: Union[str, Sequence[str], None] = '9de2183f485b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False,
                                     server_default='True'))
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
