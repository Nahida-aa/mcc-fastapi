from sqlmodel import Relationship
from api.models.base_id_model import AutoIDNameModel
from api.models.links_model import LinkTeamResource, LinkUserResource


class Resource(AutoIDNameModel, table=True):
    user_links: list[LinkUserResource] = Relationship(back_populates="resource")
    team_links: list[LinkTeamResource] = Relationship(back_populates="resource")
