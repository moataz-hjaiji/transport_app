"""Add is_active column to driver table

Revision ID: 2680a9001106
Revises: 4bdccba9120c
Create Date: 2025-07-02 20:36:47.702992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2680a9001106'
down_revision: Union[str, Sequence[str], None] = '4bdccba9120c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('driver', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.sql.expression.true()))

def downgrade():
    op.drop_column('driver', 'is_active')

