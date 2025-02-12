"""description_of_changes

Revision ID: 972e8126f402
Revises: 215942a7ca03
Create Date: 2025-01-11 20:14:44.266396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '972e8126f402'
down_revision: Union[str, None] = '215942a7ca03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dashboard_uploads', sa.Column('topic_name', sa.String(length=255), nullable=False))
    op.drop_column('dashboard_uploads', 'directory_name')
    op.alter_column('files', 'path',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_column('files', 'content')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('content', sa.TEXT(), autoincrement=False, nullable=True))
    op.alter_column('files', 'path',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.add_column('dashboard_uploads', sa.Column('directory_name', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.drop_column('dashboard_uploads', 'topic_name')
    # ### end Alembic commands ###
