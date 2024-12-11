"""2

Revision ID: 74618804b8ab
Revises: 03dc51cef475
Create Date: 2024-12-11 14:13:36.285253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '74618804b8ab'
down_revision: Union[str, None] = '03dc51cef475'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('LinkTeamIdentity',
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('identity_id', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('motivation', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['identity_id'], ['Identity.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['Team.id'], ),
    sa.PrimaryKeyConstraint('team_id', 'identity_id')
    )
    op.create_table('LinkTeamProj',
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('proj_id', sa.Integer(), nullable=False),
    sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['proj_id'], ['Proj.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['Team.id'], ),
    sa.PrimaryKeyConstraint('team_id', 'proj_id')
    )
    op.create_table('LinkTeamResource',
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['resource_id'], ['Resource.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['Team.id'], ),
    sa.PrimaryKeyConstraint('team_id', 'resource_id')
    )
    op.create_table('LinkUserIdentity',
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('identity_id', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('motivation', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['identity_id'], ['Identity.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'identity_id')
    )
    op.create_table('LinkUserProj',
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('proj_id', sa.Integer(), nullable=False),
    sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['proj_id'], ['Proj.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'proj_id')
    )
    op.create_table('LinkUserResource',
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['resource_id'], ['Resource.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'resource_id')
    )
    op.create_table('LinkUserTeam',
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['Team.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'team_id')
    )
    op.create_table('LinkUserPlatformInfoTag',
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_platform_info_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['Tag.id'], ),
    sa.ForeignKeyConstraint(['user_platform_info_id'], ['UserPlatformInfo.id'], ),
    sa.PrimaryKeyConstraint('user_platform_info_id', 'tag_id')
    )
    op.drop_table('TeamProjLink')
    op.drop_table('UserTeamLink')
    op.drop_table('UserProjLink')
    op.drop_table('UserResourceLink')
    op.drop_table('TeamIdentityLink')
    op.drop_table('TeamResourceLink')
    op.drop_table('UserPlatformInfo_Tag_Link')
    op.drop_table('UserIdentityLink')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('UserIdentityLink',
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('identity_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('level', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('motivation', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['identity_id'], ['Identity.id'], name='UserIdentityLink_identity_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], name='UserIdentityLink_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'identity_id', name='UserIdentityLink_pkey')
    )
    op.create_table('UserPlatformInfo_Tag_Link',
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_platform_info_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('tag_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['Tag.id'], name='UserPlatformInfo_Tag_Link_tag_id_fkey'),
    sa.ForeignKeyConstraint(['user_platform_info_id'], ['UserPlatformInfo.id'], name='UserPlatformInfo_Tag_Link_user_platform_info_id_fkey'),
    sa.PrimaryKeyConstraint('user_platform_info_id', 'tag_id', name='UserPlatformInfo_Tag_Link_pkey')
    )
    op.create_table('TeamResourceLink',
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('team_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('resource_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['resource_id'], ['Resource.id'], name='TeamResourceLink_resource_id_fkey'),
    sa.ForeignKeyConstraint(['team_id'], ['Team.id'], name='TeamResourceLink_team_id_fkey'),
    sa.PrimaryKeyConstraint('team_id', 'resource_id', name='TeamResourceLink_pkey')
    )
    op.create_table('TeamIdentityLink',
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('team_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('identity_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('level', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('motivation', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['identity_id'], ['Identity.id'], name='TeamIdentityLink_identity_id_fkey'),
    sa.ForeignKeyConstraint(['team_id'], ['Team.id'], name='TeamIdentityLink_team_id_fkey'),
    sa.PrimaryKeyConstraint('team_id', 'identity_id', name='TeamIdentityLink_pkey')
    )
    op.create_table('UserResourceLink',
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('resource_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['resource_id'], ['Resource.id'], name='UserResourceLink_resource_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], name='UserResourceLink_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'resource_id', name='UserResourceLink_pkey')
    )
    op.create_table('UserProjLink',
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('proj_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['proj_id'], ['Proj.id'], name='UserProjLink_proj_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], name='UserProjLink_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'proj_id', name='UserProjLink_pkey')
    )
    op.create_table('UserTeamLink',
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('team_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['Team.id'], name='UserTeamLink_team_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], name='UserTeamLink_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'team_id', name='UserTeamLink_pkey')
    )
    op.create_table('TeamProjLink',
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('team_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('proj_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['proj_id'], ['Proj.id'], name='TeamProjLink_proj_id_fkey'),
    sa.ForeignKeyConstraint(['team_id'], ['Team.id'], name='TeamProjLink_team_id_fkey'),
    sa.PrimaryKeyConstraint('team_id', 'proj_id', name='TeamProjLink_pkey')
    )
    op.drop_table('LinkUserPlatformInfoTag')
    op.drop_table('LinkUserTeam')
    op.drop_table('LinkUserResource')
    op.drop_table('LinkUserProj')
    op.drop_table('LinkUserIdentity')
    op.drop_table('LinkTeamResource')
    op.drop_table('LinkTeamProj')
    op.drop_table('LinkTeamIdentity')
    # ### end Alembic commands ###
