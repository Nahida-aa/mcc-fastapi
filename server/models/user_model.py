from datetime import datetime
from typing import List, Optional, Sequence
from pydantic import BaseModel
from sqlmodel import Field, Relationship
from server.models.base_id_model import SQLModel, TimestampMixin
from server.models.links_model import LinkUserIdentity, LinkUserPlatformInfoTag, LinkUserProj, LinkUserResource, LinkUserTeam

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
class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    avatar: str = ""
    nickname: str = ""
    email: str = Field(default="", index=True, unique=True)
    phone: str = ""  # 手机号, 通过逻辑来实现必填
    age: int | None = Field(default=None, index=True)

class UserCreate(UserBase):
    password: str
    id_card_info: Optional["IDCardInfoBase"] = None
    platform_info: Optional["UserPlatformInfoCreate"] = None

class UserUpdate(SQLModel):
    username: str | None = None
    avatar: str | None = None
    nickname: str | None = None
    email: str | None = None
    phone: str | None = None
    age: int | None = None
    password: str | None = None
    id_card_info: Optional["IDCardInfoBase"] = None
    platform_info: Optional["UserPlatformInfoUpdate"] = None

class UserPublic(UserBase):
    id: int
    is_active: bool = True
    id_card_info: Optional["IDCardInfoBase"] = None
    platform_info: Optional["UserPlatformInfoPublic"] = None

    @classmethod
    def from_orm(cls, user: "User"):
        platform_info = user.platform_info
        if platform_info:
            platform_info_public = UserPlatformInfoPublic.from_orm(platform_info)
            # print(f"{user.username}有平台信息: {platform_info_public}")

        return cls(
            id=user.id,  # type: ignore
            username=user.username,
            avatar=user.avatar,
            nickname=user.nickname,
            email=user.email,
            phone=user.phone,
            age=user.age,
            is_active=user.is_active,
            id_card_info=user.id_card_info,
            platform_info=platform_info_public,
        )

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
    @classmethod
    def from_orm_list(cls, users: Sequence["User"], count: int):
        return cls(
            data=[UserPublic.from_orm(user) for user in users],
            count=count
        )
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


class UserPlatformInfoBase(SQLModel):
    mc_experience: str = ""  # 玩 mc 多久了: 0-1年, 1-3年, 3-5年, 5-8年, 8-12年, 12年以上。默认值为 '0-1年'
    play_reason: str = ""  # 为什么会玩 mc: 可以不填。默认值为空字符串
    server_type: str = ""  # 服务器玩家 | 公益服 | 盈利服 | 多人竞技服 | 多人合作服。默认值为 '服务器玩家'
    desired_partners: str = ""  # 平台内想结识怎样的伙伴: 拒绝社交|服务器伙伴|同好建筑内容的伙伴|同好生存内容的伙伴|同好冒险内容的伙伴|同好科技内容的伙伴
class UserPlatformInfoCreate(UserPlatformInfoBase):
    favorite_content: list[str] = []
class UserPlatformInfoPublic(UserPlatformInfoBase):
    favorite_content: list[str] = []
    @classmethod
    def from_orm(cls, user_platform_info: "UserPlatformInfo"):
        favorite_content = []
        if user_platform_info.favorite_content:
            favorite_content = [link.tag.name for link in user_platform_info.favorite_content]
        return cls(
            mc_experience=user_platform_info.mc_experience,
            play_reason=user_platform_info.play_reason,
            server_type=user_platform_info.server_type,
            desired_partners=user_platform_info.desired_partners,
            favorite_content=favorite_content
        )
class UserPlatformInfoUpdate(BaseModel):
    mc_experience: str | None = None
    play_reason: str | None = None
    server_type: str | None = None
    desired_partners: str | None = None
    favorite_content: list[str] | None = None
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
