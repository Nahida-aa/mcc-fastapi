from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime
# SQLite 不支持 JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship, SQLModel, JSON

from api.routes.user.schemas import FavoriteContent

# from api.lib.database import Base


class UserIdentityLink(SQLModel, table=True):
    user_id: int|None = Field(default=None, foreign_key="user.id", primary_key=True)
    identity_id: Optional[int] = Field(default=None, foreign_key="identity.id", primary_key=True)
    
class User(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    last_login: datetime | None = None
    is_superuser: bool = False
    is_staff: bool = False
    is_active: bool = True
    
    avatar: str = ""
    username: str = Field(unique=True, index=True)
    hashed_password: str
    phone: str 
    id_card_info: Optional["IDCardInfo"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False}) # 身份证信息
    
    email: str = Field(default="", index=True, unique=True)
    age: int | None = None
    gender: str | None = None
    nickname: str = ""
    door_number: int | None = None
    
    
    # teams: List["Team"] = Relationship(back_populates="owner")
    
    identities: list["Identity"] = Relationship(back_populates="users", link_model=UserIdentityLink) # 平台认证的身份
    projs: list["Proj"] = Relationship(back_populates="owner_user")

class Proj(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    owner_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner_team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    
    # 关系属性, 不直接代表数据库中的列, 们的值也不是像整数这样的单个值。它们的值是实际的整个相关对象
    owner_user: Optional[User] = Relationship(back_populates="projs")
    owner_team: Optional["Team"] = Relationship(back_populates="projs")

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")

    owner: Optional[User] = Relationship(back_populates="teams")
    members: List["User"] = Relationship(back_populates="team")

class Identity(SQLModel, table=True): # 
    id: int|None = Field(default=None, primary_key=True)
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)
    name: str  # 身份名称: 创作者, 投资者, 施工者, 鉴赏者, ...
    level: int  # 身份评级
    status: str  # 身份状态
    motivation: str  # 身份动机: 初心
    
    users: List[User] = Relationship(back_populates="identities", link_model=UserIdentityLink)


class Resource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    owner_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner_team_id: Optional[int] = Field(default=None, foreign_key="team.id")

    owner_user: Optional[User] = Relationship(back_populates="resources", foreign_keys=[owner_user_id])
    owner_team: Optional[Team] = Relationship(back_populates="resources", foreign_keys=[owner_team_id])

    owner: Optional[User] = Relationship(back_populates="resources")
    
class IDCardInfo(SQLModel, table=True): # 身份证信息
    id: int|None = Field(default=None, primary_key=True)
    user_id: int|None = Field(default=None, foreign_key="user.id")
    id_card_number: str = Field(index=True, unique=True)
    id_card_holder: str = "self"  # 新添加的字段，用于表示身份证类型
    is_real_name: bool = False # 是否实名认证
    front_image_url: str|None = None
    back_image_url: str|None = None

    user: User|None = Relationship(back_populates="id_card_info")