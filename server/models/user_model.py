from datetime import datetime
from typing import List, Optional, Sequence
from sqlmodel import Field, Relationship
from server.models.base_id_model import SQLModel, TimestampMixin
from server.models.links_model import LinkUserIdentity, LinkUserPlatformInfoTag, LinkUserProj, LinkUserResource, LinkUserTeam


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    avatar: str = ""
    nickname: str = ""
    email: str = Field(default="", index=True, unique=True)
    phone: str = ""  # 手机号, 通过逻辑来实现必填
    age: int | None = Field(default=None, index=True)

class UserCreate(UserBase):
    password: str
    id_card_info: Optional["IDCardInfo"] = None
    platform_info: Optional["UserPlatformInfo"] = None

class UserUpdate(SQLModel):
    username: str | None = None
    avatar: str | None = None
    nickname: str | None = None
    email: str | None = None
    phone: str | None = None
    age: int | None = None
    password: str | None = None
    id_card_info: Optional["IDCardInfo"] = None
    platform_info: Optional["UserPlatformInfo"] = None

class UserPublic(UserBase):
    id: int
    is_active: bool = True
    id_card_info: Optional["IDCardInfo"] = None
    platform_info: Optional["UserPlatformInfo"] = None
class UsersPublic(SQLModel):
    # data: list[UserPublic]
    data: Sequence["UserPublic"]
    count: int
class User(UserBase, TimestampMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    last_login: datetime | None = None
    is_superuser: bool = False
    is_staff: bool = False
    is_active: bool = True
    hashed_password: str
    gender: str | None = None
    id_card_info: Optional["IDCardInfo"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})
    platform_info: Optional["UserPlatformInfo"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})

    home: Optional["Home"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})
    team_links: list[LinkUserTeam] = Relationship(back_populates="user")
    identity_links: list[LinkUserIdentity] = Relationship(back_populates="user")
    proj_links: list[LinkUserProj] = Relationship(back_populates="user")
    resource_links: list[LinkUserResource] = Relationship(back_populates="user")

class IDCardInfo(SQLModel, table=True):  # 身份证信息, 一对一关系, 主表不用存数据
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="User.id")
    id_card_number: str = Field(index=True, unique=True)
    id_card_holder: str = "self"  # 新添加的字段，用于表示身份证类型
    is_real_name: bool = False  # 是否实名认证
    front_image_url: str | None = None
    back_image_url: str | None = None
    user: User | None = Relationship(back_populates="id_card_info")

class UserPlatformInfo(SQLModel, table=True):  # 平台信息, 类似于调查问卷, 我认为易变
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="User.id")
    mc_experience: str = ""  # 玩 mc 多久了: 0-1年, 1-3年, 3-5年, 5-8年, 8-12年, 12年以上。默认值为 '0-1年'
    play_reason: str = ""  # 为什么会玩 mc: 可以不填。默认值为空字符串
    server_type: str = ""  # 服务器玩家 | 公益服 | 盈利服 | 多人竞技服 | 多人合作服。默认值为 '服务器玩家'
    favorite_content: list[LinkUserPlatformInfoTag] = Relationship(back_populates="user_platform_info")
    desired_partners: str = ""  # 平台内想结识怎样的伙伴: 拒绝社交|服务器伙伴|同好建筑内容的伙伴|同好生存内容的伙伴|同好冒险内容的伙伴|同好科技内容的伙伴
    user: User | None = Relationship(back_populates="platform_info")

class Home(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="User.id")
    door_number: int | None = None
    user: Optional[User] = Relationship(back_populates="home")