from sqlmodel import Field, Relationship
from server.models.base_id_model import SQLModel
from server.models import LinkUserPlatformInfoTag


class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = ""
    user_platform_info_links: list[LinkUserPlatformInfoTag] = Relationship(back_populates="tag")