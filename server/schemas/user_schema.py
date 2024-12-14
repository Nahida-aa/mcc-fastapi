from typing import Optional, Sequence
from sqlmodel import Field, SQLModel
from server.models.user_model import IDCardInfoBase, User, UserBase, UserPlatformInfo, UserPlatformInfoBase


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
    # password: str | None = None
    

class UserUpdateWithAll(UserUpdate):
    id_card_info: Optional["IDCardInfoBase"] = None
    platform_info: Optional["UserPlatformInfoUpdate"] = None
class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)
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
            followers_count=user.followers_count,
            following_count=user.following_count,
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
        
class IDCardInfoUpdate(SQLModel):
    id_card_number: str | None = None
    id_card_holder: str | None = None
    is_real_name: bool | None = None
    front_image_url: str | None = None
    back_image_url: str | None = None
    
    
class UserPlatformInfoCreate(UserPlatformInfoBase):
    favorite_content: list[str] = []
class UserPlatformInfoPublic(UserPlatformInfoBase):
    favorite_content: list[str] = []
    @classmethod
    def from_orm(cls, user_platform_info: "UserPlatformInfo")->"UserPlatformInfoPublic":
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
class UserPlatformInfoUpdate(SQLModel):
    mc_experience: str | None = None
    play_reason: str | None = None
    server_type: str | None = None
    desired_partners: str | None = None
    favorite_content: list[str] | None = None
