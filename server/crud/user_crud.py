from fastapi import HTTPException
from sqlmodel import Session, select
from server.core.security import get_password_hash
from server.crud.base_crud import CRUDBase
from server.models.user_model import User, UserCreate, UserUpdate
from fastapi import HTTPException, Path, status

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, *, username: str, db_session: Session) -> User|None:
        # db_session = db_session or super().get_db()
        statement = select(User).where(User.username == username)
        return db_session.exec(statement).one_or_none()
    def create(self, *, obj_in: UserCreate, db_session: Session) -> User:
        db_obj = User.model_validate(obj_in, update={"hashed_password": get_password_hash(obj_in.password)})
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj
    
user = CRUDUser(User)

from server.models.user_model import User, UserCreate, IDCardInfo, UserPlatformInfo, LinkUserPlatformInfoTag
from server.models.tag_model import Tag
from server.core.security import get_password_hash

def create_user(user: UserCreate, db: Session,):
    # 检查用户名是否已存在
    db_user = db.exec(select(User).where(User.username == user.username)).one_or_none()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    # 创建新用户
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        phone=user.phone,
        age=user.age,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=False,
        is_staff=False,
    )
    
    # 处理 IDCardInfo
    if user.id_card_info:
        db_id_card_info = IDCardInfo(
            id_card_number=user.id_card_info.id_card_number,
            id_card_holder=user.id_card_info.id_card_holder,
            is_real_name=user.id_card_info.is_real_name,
            front_image_url=user.id_card_info.front_image_url,
            back_image_url=user.id_card_info.back_image_url,
            user=db_user
        )
        db.add(db_id_card_info)
    
    # 处理 UserPlatformInfo
    if user.platform_info:
        db_platform_info = UserPlatformInfo(
            mc_experience=user.platform_info.mc_experience,
            play_reason=user.platform_info.play_reason,
            server_type=user.platform_info.server_type,
            desired_partners=user.platform_info.desired_partners,
            user=db_user
        )
        db.add(db_platform_info)
    
        # 处理 favorite_content
        if user.platform_info.favorite_content:
            for tag_name in user.platform_info.favorite_content:
                tag = db.exec(select(Tag).where(Tag.name == tag_name)).one_or_none()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                    db.commit()
                    db.refresh(tag)
                link = LinkUserPlatformInfoTag(user_platform_info=db_platform_info, tag=tag)
                db.add(link)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# def get_users(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(User).offset(skip).limit(limit).all()

# def get_user(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()

# def update_user(db: Session, user_id: int, user_update: UserUpdate):
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
#     for key, value in user_update.dict(exclude_unset=True).items():
#         setattr(db_user, key, value)
    
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def delete_user(db: Session, user_id: int):
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
#     db.delete(db_user)
#     db.commit()
#     return db_user