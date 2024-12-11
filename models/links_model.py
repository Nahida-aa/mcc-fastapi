from sqlmodel import Field, Relationship
from api.models.base_id_model import TimestampMixin
from api.models import Identity, Proj, Resource,  Tag, Team, User, UserPlatformInfo

class LinkUserTeam(TimestampMixin, table=True):
    user_id: int | None = Field(default=None, foreign_key="User.id", primary_key=True)
    team_id: int | None = Field(default=None, foreign_key="Team.id", primary_key=True)
    role: str = "member"  # 角色，例如：owner, member, admin
    team: "Team" = Relationship(back_populates="user_links")
    user: "User" = Relationship(back_populates="team_links")

class LinkUserIdentity(TimestampMixin, table=True):
    user_id: int | None = Field(default=None, foreign_key="User.id", primary_key=True)
    identity_id: int | None = Field(default=None, foreign_key="Identity.id", primary_key=True)
    level: int  # 身份评级
    status: str  # 身份状态
    motivation: str  # 身份动机: 初心
    identity: "Identity" = Relationship(back_populates="user_links")
    user: "User" = Relationship(back_populates="identity_links")

class LinkTeamIdentity(TimestampMixin, table=True):
    team_id: int | None = Field(default=None, foreign_key="Team.id", primary_key=True)
    identity_id: int | None = Field(default=None, foreign_key="Identity.id", primary_key=True)
    level: int  # 身份评级
    status: str  # 身份状态
    motivation: str  # 身份动机: 初心
    identity: "Identity" = Relationship(back_populates="team_links")
    team: "Team" = Relationship(back_populates="identity_links")

class LinkUserProj(TimestampMixin, table=True):
    user_id: int | None = Field(default=None, foreign_key="User.id", primary_key=True)
    proj_id: int | None = Field(default=None, foreign_key="Proj.id", primary_key=True)
    role: str = "member"  # 角色，例如：owner, member, admin
    proj: "Proj" = Relationship(back_populates="user_links")
    user: "User" = Relationship(back_populates="proj_links")

class LinkTeamProj(TimestampMixin, table=True):
    team_id: int | None = Field(default=None, foreign_key="Team.id", primary_key=True)
    proj_id: int | None = Field(default=None, foreign_key="Proj.id", primary_key=True)
    role: str = "member"  # 角色，例如：owner, member, admin
    proj: "Proj" = Relationship(back_populates="team_links")
    team: "Team" = Relationship(back_populates="proj_links")

class LinkUserResource(TimestampMixin, table=True):
    user_id: int | None = Field(default=None, foreign_key="User.id", primary_key=True)
    resource_id: int | None = Field(default=None, foreign_key="Resource.id", primary_key=True)
    role: str = "member"  # 角色，例如：owner, member, admin
    resource: "Resource" = Relationship(back_populates="user_links")
    user: "User" = Relationship(back_populates="resource_links")

class LinkTeamResource(TimestampMixin, table=True):
    team_id: int | None = Field(default=None, foreign_key="Team.id", primary_key=True)
    resource_id: int | None = Field(default=None, foreign_key="Resource.id", primary_key=True)
    role: str = "member"  # 角色，例如：owner, member, admin
    resource: "Resource" = Relationship(back_populates="team_links")
    team: "Team" = Relationship(back_populates="resource_links")

class LinkUserPlatformInfoTag(TimestampMixin, table=True):
    user_platform_info_id: int | None = Field(default=None, foreign_key="UserPlatformInfo.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="Tag.id", primary_key=True)
    user_platform_info: "UserPlatformInfo" = Relationship(back_populates="favorite_content")
    tag: "Tag" = Relationship(back_populates="user_platform_info_links")
