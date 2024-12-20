"""8

Revision ID: 96dabecd375f
Revises: 31317b42142b
Create Date: 2024-12-17 14:40:13.682281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = '96dabecd375f'
down_revision: Union[str, None] = '31317b42142b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_Identity_name', table_name='Identity')
    op.create_index(op.f('ix_Identity_name'), 'Identity', ['name'], unique=True)
    op.drop_index('ix_Proj_name', table_name='Proj')
    op.create_index(op.f('ix_Proj_name'), 'Proj', ['name'], unique=True)
    op.drop_index('ix_Resource_name', table_name='Resource')
    op.create_index(op.f('ix_Resource_name'), 'Resource', ['name'], unique=True)
    op.drop_index('ix_Team_name', table_name='Team')
    op.create_index(op.f('ix_Team_name'), 'Team', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Team_name'), table_name='Team')
    op.create_index('ix_Team_name', 'Team', ['name'], unique=False)
    op.drop_index(op.f('ix_Resource_name'), table_name='Resource')
    op.create_index('ix_Resource_name', 'Resource', ['name'], unique=False)
    op.drop_index(op.f('ix_Proj_name'), table_name='Proj')
    op.create_index('ix_Proj_name', 'Proj', ['name'], unique=False)
    op.drop_index(op.f('ix_Identity_name'), table_name='Identity')
    op.create_index('ix_Identity_name', 'Identity', ['name'], unique=False)
    # ### end Alembic commands ###
