"""Add path column to files table

Revision ID: 215942a7ca03
Revises: aec8f0bacff7
Create Date: 2025-01-11 20:05:43.743377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '215942a7ca03'
down_revision: Union[str, None] = 'aec8f0bacff7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from sqlalchemy import text

def upgrade():
    # Get the database connection
    conn = op.get_bind()

    # Use text() to execute the raw SQL
    result = conn.execute(text("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'files' AND column_name = 'path'
    """))
    
    # If the 'path' column doesn't exist, add it
    if not result.fetchone():  # Column doesn't exist
        op.add_column('files', sa.Column('path', sa.String(length=255), nullable=True))

    # Optionally, update existing rows with a default value for 'path' if necessary
    op.execute("UPDATE files SET path = 'default_value' WHERE path IS NULL")

    # Alter the column to be non-nullable after updating the existing rows
    op.alter_column('files', 'path', nullable=False)

def downgrade():
    # Drop the 'path' column during downgrade
    op.drop_column('files', 'path')
