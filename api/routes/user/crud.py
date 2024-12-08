# from sqlalchemy.orm import Session
from sqlmodel import Field, Session, SQLModel, create_engine, select
from api.routes.security import get_password_hash
from . import schemas, models


def get_user(db: Session, user_id: int):
    # return db.query(models.User).filter(models.User.id == user_id).first()
    return db.exec(select(models.User).where(models.User.id == user_id)).first()
def get_user_by_username(db: Session, username: str):
    # return db.query(models.User).filter(models.User.username == username).first()
    return db.exec(select(models.User).where(models.User.username == username)).first()
def get_users(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    return db.exec(select(models.User).offset(skip).limit(limit)).all()

def create_user(db: Session, user: schemas.UserCreate_In):
    fake_hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password, phone=user.phone, avatar=user.avatar)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    id_card_info = models.IDCardInfo( # 身份证信息
        user_id=db_user.id,
        id_card_number=user.id_card_info.id_card_number,
        id_card_holder=user.id_card_info.id_card_holder,
        front_image_url=user.id_card_info.front_image_url,
        back_image_url=user.id_card_info.back_image_url
    )
    db.add(id_card_info)
    db.commit()
    db.refresh(id_card_info)
    
    db_user.id_card_info = id_card_info
    
    # 检查 UserPlatformInfo 的完整性，并分配相应的身份，并分配 "鉴赏者" 身份
    platform_info_url = f"{db_user.id}/platform_info.json"
    if check_platform_info_complete(platform_info_url):
        appreciator_identity = models.Identity(
            name="鉴赏者",
            level=0,
            status="active",
            motivation="平台",
        )
        db.add(appreciator_identity)
        db.commit()
        db.refresh(appreciator_identity)
        user_identity_link = models.UserIdentityLink(user_id=db_user.id, identity_id=appreciator_identity.id)
        db.add(user_identity_link)
        db.commit()

    db.refresh(db_user)
    return db_user
def check_platform_info_complete(url: str) -> bool:
    # 这里实现检查外部文件完整性的逻辑
    # 例如，读取 JSON 文件并检查所有必填字段是否存在
    return True

def get_projs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Proj).offset(skip).limit(limit).all()


# def create_user_proj(db: Session, proj: schemas.ProjCreateIn, user_id: int):
#     db_proj = models.Proj(**proj.model_dump(), owner_id=user_id)
#     db.add(db_proj)
#     db.commit()
#     db.refresh(db_proj)
#     return db_proj