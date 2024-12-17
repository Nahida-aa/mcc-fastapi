from datetime import datetime
from typing import List, Optional, Sequence
from pydantic import BaseModel
from sqlmodel import Field, Relationship
from server.models.base_id_model import AutoIDNameModel, SQLModel, TimestampMixin
from server.models import LinkUserFollow, LinkTeamFollow, LinkUserIdentity, LinkUserPlatformInfoTag, LinkUserProj, LinkUserResource, LinkUserTeam

class IDCardInfoBase(SQLModel):
    id_card_number: str = Field(index=True, unique=True)
    id_card_holder: str = "self"
    is_real_name: bool = False
    front_image_url: str | None = None
    back_image_url: str | None = None

class IDCardInfo(IDCardInfoBase, table=True):  # 身份证信息, 一对一关系, 主表不用存数据
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="User.id")
    user: Optional["User"] = Relationship(back_populates="id_card_info")
    
class UserBase(AutoIDNameModel):
    image: str = ""
    nickname: str = ""
    email: str | None = Field(default=None, index=True, unique=True)
    phone: str = ""  # 手机号, 通过逻辑来实现必填
    age: int | None = Field(default=None, index=True)
    followers_count: int = 0 # 粉丝数
    following_count: int = 0 # 关注的用户(包括团队)数

class User(UserBase, table=True):
    last_login: datetime | None = None
    is_superuser: bool = False
    is_staff: bool = False
    is_active: bool = True
    hashed_password: str
    gender: str | None = None
    id_card_info: Optional["IDCardInfo"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})
    platform_info: Optional["UserPlatformInfo"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})
    
    home: Optional["Home"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})

    # follower_links: list["LinkUserFollow"] = Relationship(back_populates="followed", sa_relationship_kwargs={"foreign_keys": [LinkUserFollow.followed_id]}) # 粉丝s
    # following_links: list["LinkUserFollow"] = Relationship(back_populates="follower", sa_relationship_kwargs={ "foreign_keys": [LinkUserFollow.follower_id]}) # 关注的用户s
    team_following_links: list["LinkTeamFollow"] = Relationship(back_populates="user") # 关注的团队s
    
    team_links: list[LinkUserTeam] = Relationship(back_populates="user")
    identity_links: list[LinkUserIdentity] = Relationship(back_populates="user")
    proj_links: list[LinkUserProj] = Relationship(back_populates="user")
    resource_links: list[LinkUserResource] = Relationship(back_populates="user")


class UserPlatformInfoBase(SQLModel):
    mc_experience: str = ""  # 玩 mc 多久了: 0-1年, 1-3年, 3-5年, 5-8年, 8-12年, 12年以上。默认值为 '0-1年'
    play_reason: str = ""  # 为什么会玩 mc: 可以不填。默认值为空字符串
    server_type: str = ""  # 服务器玩家 | 公益服 | 盈利服 | 多人竞技服 | 多人合作服。默认值为 '服务器玩家'
    desired_partners: str = ""  # 平台内想结识怎样的伙伴: 拒绝社交|服务器伙伴|同好建筑内容的伙伴|同好生存内容的伙伴|同好冒险内容的伙伴|同好科技内容的伙伴

class UserPlatformInfo(UserPlatformInfoBase, table=True):  # 平台信息, 类似于调查问卷, 我认为易变
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="User.id")
    
    favorite_content: list[LinkUserPlatformInfoTag] = Relationship(back_populates="user_platform_info") # 建筑, 生存, 冒险, 科技
    user: User | None = Relationship(back_populates="platform_info")

class Home(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="User.id")
    door_number: int | None = None
    user: Optional[User] = Relationship(back_populates="home")
