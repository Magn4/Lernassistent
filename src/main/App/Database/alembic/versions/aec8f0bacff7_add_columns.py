"""Add columns

Revision ID: aec8f0bacff7
Revises: 
Create Date: 2025-01-11 19:47:00.557366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aec8f0bacff7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Step 1: Add the 'path' column as nullable (it can contain null initially)
    op.add_column('files', sa.Column('path', sa.String(length=255), nullable=True))
    
    # Step 2: Update existing rows to set a default value for 'path'
    op.execute("UPDATE files SET path = 'default_value' WHERE path IS NULL")
    
    # Step 3: Alter the column to be non-nullable after updating the existing rows
    op.alter_column('files', 'path', nullable=False)

def downgrade():
    # Drop the 'path' column during downgrade
    op.drop_column('files', 'path')
