from sqlmodel import Relationship
from server.models.base_id_model import AutoIDNameModel
from server.models import LinkTeamIdentity, LinkTeamProj, LinkTeamResource, LinkUserTeam


class Team(AutoIDNameModel, table=True):
    user_links: list[LinkUserTeam] = Relationship(back_populates="team")
    identity_links: list[LinkTeamIdentity] = Relationship(back_populates="team")
    proj_links: list[LinkTeamProj] = Relationship(back_populates="team")
    resource_links: list[LinkTeamResource] = Relationship(back_populates="team")