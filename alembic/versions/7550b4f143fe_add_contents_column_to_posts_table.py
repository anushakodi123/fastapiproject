"""add contents column to posts table

Revision ID: 7550b4f143fe
Revises: 947f4e96b1f6
Create Date: 2025-07-03 01:31:57.950893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7550b4f143fe'
down_revision: Union[str, Sequence[str], None] = '947f4e96b1f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))   
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
