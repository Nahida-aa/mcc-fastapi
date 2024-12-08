"""sqlmodel

Revision ID: cca69e1db101
Revises: 831c6e904a80
Create Date: 2024-12-01 22:47:21.374350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cca69e1db101'
down_revision: Union[str, None] = '831c6e904a80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar', sa.String(), nullable=False))
    op.alter_column('user', 'nickname',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'nickname',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('user', 'avatar')
    # ### end Alembic commands ###
