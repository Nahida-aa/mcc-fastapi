from typing import Optional
from pydantic import BaseModel


class ProjBase(BaseModel):
    name: str
    description: str | None = None


class ProjCreateIn(ProjBase):
    pass


class Proj(ProjBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    avatar: str = ""
    nickname: str = ""
    email: str = ""

class IDCardInfoBase(BaseModel):
    id_card_number: str
    id_card_holder: str = "self" # 身份证人: 自己, 监护人
    front_image_url: Optional[str] = None
    back_image_url: Optional[str] = None
class IDCardInfo_Out(IDCardInfoBase):
    is_real_name: bool
    id: int
    user_id: int

class FavoriteContent(BaseModel): # 喜欢的内容 TODO: 预期可能经常发生变化
    building: bool = False # 建筑
    survival: bool = False # 生存
    adventure: bool = False # 冒险
    technology: bool = False # 科技
    
    class Config:
        from_attributes = True
class UserPlatformInfo(BaseModel): # 平台信息 TODO: 预期可能经常发生变化
    mc_experience: str = "" # 玩 mc 多久了: 0-1年, 1-3年, 3-5年, 5-8年, 8-12年, 12年以上。默认值为 '0-1年'
    play_reason: str = "" # 为什么会玩 mc: 可以不填。默认值为空字符串
    server_type: str = "" # 服务器玩家 | 公益服 | 盈利服 | 多人竞技服 | 多人合作服。默认值为 '服务器玩家'
    favorite_content: FavoriteContent = FavoriteContent()
    desired_partners: str = "" # 平台内想结识怎样的伙伴: 拒绝社交|服务器伙伴|同好建筑内容的伙伴|同好生存内容的伙伴|同好冒险内容的伙伴|同好科技内容的伙伴
class UserCreate_In(UserBase):
    password: str
    phone: str
    id_card_info: IDCardInfoBase
    platform_info: UserPlatformInfo = UserPlatformInfo()
class UserCreate_Out(UserBase):
    id: int
    is_active: bool
    id_card_info: IDCardInfoBase
    platform_info: UserPlatformInfo = UserPlatformInfo()
class User(UserBase):
    id: int
    
    is_active: bool
    Projs: list[Proj] = []

    class Config:
        from_attributes = True # from_attributes\orm_mode 将告诉 Pydantic 模型即使数据不是 dict，而是 ORM 模型（或任何其他具有属性的任意对象），也要读取数据
