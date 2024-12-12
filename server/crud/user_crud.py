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
    def get_by_email(self, *, email: str, db_session: Session) -> User|None:
        statement = select(User).where(User.email == email)
        return db_session.exec(statement).one_or_none()
    def create(self, *, obj_in: UserCreate, db_session: Session):
        # 创建新用户
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            phone=obj_in.phone,
            age=obj_in.age,
            hashed_password=get_password_hash(obj_in.password),
            is_active=True,
            is_superuser=False,
            is_staff=False,
        )
        print(f"db_obj: {db_obj}")
        
        # 处理 IDCardInfo
        if obj_in.id_card_info:
            db_id_card_info = IDCardInfo(
                id_card_number=obj_in.id_card_info.id_card_number,
                id_card_holder=obj_in.id_card_info.id_card_holder,
                is_real_name=obj_in.id_card_info.is_real_name,
                front_image_url=obj_in.id_card_info.front_image_url,
                back_image_url=obj_in.id_card_info.back_image_url,
                user=db_obj
            )
            db_session.add(db_id_card_info)
            print(f"db_id_card_info: {db_id_card_info}")
        
        # 处理 UserPlatformInfo
        if obj_in.platform_info:
            db_platform_info = UserPlatformInfo(
                mc_experience=obj_in.platform_info.mc_experience,
                play_reason=obj_in.platform_info.play_reason,
                server_type=obj_in.platform_info.server_type,
                desired_partners=obj_in.platform_info.desired_partners,
                user=db_obj
            )
            db_session.add(db_platform_info)
            print(f"db_platform_info: {db_platform_info}")
            
            # 处理 favorite_content
            if obj_in.platform_info.favorite_content:
                for tag_name in obj_in.platform_info.favorite_content:
                    tag = db_session.exec(select(Tag).where(Tag.name == tag_name)).one_or_none()
                    if not tag:
                        tag = Tag(name=tag_name)
                        db_session.add(tag)
                        db_session.commit()
                        db_session.refresh(tag)
                    link = LinkUserPlatformInfoTag(user_platform_info=db_platform_info, tag=tag)
                    db_session.add(link)
                print(f"link: {link}")
        
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj
    
user = CRUDUser(User)

from server.models.user_model import User, UserCreate, IDCardInfo, UserPlatformInfo, LinkUserPlatformInfoTag
from server.models.tag_model import Tag
from server.core.security import get_password_hash

def create_user(user_in: UserCreate, db: Session,):
    # 创建新用户
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        phone=user_in.phone,
        age=user_in.age,
        hashed_password=get_password_hash(user_in.password),
        is_active=True,
        is_superuser=False,
        is_staff=False,
    )
    
    # 处理 IDCardInfo
    if user_in.id_card_info:
        db_id_card_info = IDCardInfo(
            id_card_number=user_in.id_card_info.id_card_number,
            id_card_holder=user_in.id_card_info.id_card_holder,
            is_real_name=user_in.id_card_info.is_real_name,
            front_image_url=user_in.id_card_info.front_image_url,
            back_image_url=user_in.id_card_info.back_image_url,
            user=db_user
        )
        db.add(db_id_card_info)
    
    # 处理 UserPlatformInfo
    if user_in.platform_info:
        db_platform_info = UserPlatformInfo(
            mc_experience=user_in.platform_info.mc_experience,
            play_reason=user_in.platform_info.play_reason,
            server_type=user_in.platform_info.server_type,
            desired_partners=user_in.platform_info.desired_partners,
            user=db_user
        )
        db.add(db_platform_info)
    
        # 处理 favorite_content
        if user_in.platform_info.favorite_content:
            for tag_name in user_in.platform_info.favorite_content:
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