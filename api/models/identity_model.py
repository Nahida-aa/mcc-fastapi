from sqlmodel import Relationship
from api.models.base_id_model import AutoIDNameModel
from api.models.links_model import LinkTeamIdentity, LinkUserIdentity


class Identity(AutoIDNameModel, table=True):  # 身份名称: 创作者, 投资者, 施工者, 鉴赏者, ...
    user_links: list[LinkUserIdentity] = Relationship(back_populates="identity")
    team_links: list[LinkTeamIdentity] = Relationship(back_populates="identity")
