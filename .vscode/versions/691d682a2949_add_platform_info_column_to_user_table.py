"""Add platform_info column to User table

Revision ID: 691d682a2949
Revises: cca69e1db101
Create Date: 2024-12-09 20:21:08.252412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '691d682a2949'
down_revision: Union[str, None] = 'cca69e1db101'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resource',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resource_name'), 'resource', ['name'], unique=False)
    op.create_table('team',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_team_name'), 'team', ['name'], unique=False)
    op.create_table('home',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('door_number', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teamidentitylink',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('identity_id', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('motivation', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['identity_id'], ['identity.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('team_id', 'identity_id')
    )
    op.create_table('teamprojlink',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('proj_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['proj_id'], ['proj.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('team_id', 'proj_id')
    )
    op.create_table('teamresourcelink',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('team_id', 'resource_id')
    )
    op.create_table('userprojlink',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('proj_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['proj_id'], ['proj.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'proj_id')
    )
    op.create_table('userresourcelink',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'resource_id')
    )
    op.create_table('userteamlink',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'team_id')
    )
    op.add_column('identity', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('identity', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('identity', sa.Column('description', sa.String(), nullable=False))
    op.create_index(op.f('ix_identity_name'), 'identity', ['name'], unique=False)
    op.drop_column('identity', 'total_interactions')
    op.drop_column('identity', 'updated')
    op.drop_column('identity', 'level')
    op.drop_column('identity', 'status')
    op.drop_column('identity', 'motivation')
    op.drop_column('identity', 'created')
    op.add_column('proj', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('proj', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.alter_column('proj', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_index('ix_proj_description', table_name='proj')
    op.drop_constraint('proj_owner_id_fkey', 'proj', type_='foreignkey')
    op.drop_column('proj', 'owner_id')
    op.add_column('user', sa.Column('platform_info', sa.String(), nullable=False, server_default='{}'))
    op.alter_column('user', 'phone',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_index(op.f('ix_user_age'), 'user', ['age'], unique=False)
    op.drop_column('user', 'door_number')
    op.add_column('useridentitylink', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('useridentitylink', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('useridentitylink', sa.Column('level', sa.Integer(), nullable=False))
    op.add_column('useridentitylink', sa.Column('status', sa.String(), nullable=False))
    op.add_column('useridentitylink', sa.Column('motivation', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('useridentitylink', 'motivation')
    op.drop_column('useridentitylink', 'status')
    op.drop_column('useridentitylink', 'level')
    op.drop_column('useridentitylink', 'updated_at')
    op.drop_column('useridentitylink', 'created_at')
    op.add_column('user', sa.Column('door_number', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_user_age'), table_name='user')
    op.alter_column('user', 'phone',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('user', 'platform_info')
    op.add_column('proj', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('proj_owner_id_fkey', 'proj', 'user', ['owner_id'], ['id'])
    op.create_index('ix_proj_description', 'proj', ['description'], unique=False)
    op.alter_column('proj', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('proj', 'updated_at')
    op.drop_column('proj', 'created_at')
    op.add_column('identity', sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('identity', sa.Column('motivation', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('identity', sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('identity', sa.Column('level', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('identity', sa.Column('updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('identity', sa.Column('total_interactions', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_identity_name'), table_name='identity')
    op.drop_column('identity', 'description')
    op.drop_column('identity', 'updated_at')
    op.drop_column('identity', 'created_at')
    op.drop_table('userteamlink')
    op.drop_table('userresourcelink')
    op.drop_table('userprojlink')
    op.drop_table('teamresourcelink')
    op.drop_table('teamprojlink')
    op.drop_table('teamidentitylink')
    op.drop_table('home')
    op.drop_index(op.f('ix_team_name'), table_name='team')
    op.drop_table('team')
    op.drop_index(op.f('ix_resource_name'), table_name='resource')
    op.drop_table('resource')
    # ### end Alembic commands ###
