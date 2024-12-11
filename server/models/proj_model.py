from sqlmodel import Relationship
from server.models.base_id_model import AutoIDNameModel
from server.models import LinkTeamProj, LinkUserProj


class Proj(AutoIDNameModel, table=True):
    user_links: list[LinkUserProj] = Relationship(back_populates="proj")
    team_links: list[LinkTeamProj] = Relationship(back_populates="proj")
