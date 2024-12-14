from sqlmodel import Relationship
from server.models.base_id_model import AutoIDNameModel
from server.models import LinkTeamIdentity, LinkTeamProj, LinkTeamResource, LinkUserTeam, LinkTeamFollow


class Team(AutoIDNameModel, table=True):
    user_links: list[LinkUserTeam] = Relationship(back_populates="team")
    identity_links: list[LinkTeamIdentity] = Relationship(back_populates="team")
    proj_links: list[LinkTeamProj] = Relationship(back_populates="team")
    resource_links: list[LinkTeamResource] = Relationship(back_populates="team")
    
    follower_links: list["LinkTeamFollow"] = Relationship(back_populates="team") # 粉丝
    followers_count: int = 0
