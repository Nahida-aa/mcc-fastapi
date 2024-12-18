
from server.utils.exceptions import (
    # IdNotFoundException,
    SelfFollowedException,
    # UserFollowedException,
    # UserNotFollowedException,
    # UserSelfDeleteException,
)
from datetime import timedelta
from typing import Annotated
from fastapi import (APIRouter,
    Body,
    Depends,
    File, HTTPException,
    Query,
    Response,
    UploadFile,
    status,)
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Session, col, delete, func, select


from server import crud
from server.deps.security_dep import get_current_user,  CurrentUser
from server.models.links_model import LinkUserFollow
from server.models.user_model import IDCardInfo,  User,  UserPlatformInfo
from server.schemas.user_schema import IDCardInfoUpdate, UpdatePassword, UserCreate, UserPlatformInfoPublic, UserPlatformInfoUpdate, UserPublic, UserUpdate, UsersPublic
from server.deps import SessionDep, user_deps
from server.deps.user_deps import CheckUserExists


router = APIRouter(prefix="/api/py")

@router.get("/user", tags=["user"])
def read_user(current_user: User = Depends(get_current_user))->UserPublic:
    return UserPublic.from_orm(current_user)
@router.get("/user/{name}", tags=["user"])
def read_user_by_name(name: str, db: SessionDep)->UserPublic:
    user = crud.user.get_by_name(db_session=db, name=name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserPublic.from_orm(user)

@router.get("/users", tags=["user"]
    # dependencies=[Depends(get_current_active_superuser)],
    # response_model=list[UserPublic],
)
def read_users(db: SessionDep, skip: int = 0, limit: int = 100)->UsersPublic:
    count_statement = select(func.count()).select_from(User)
    count = db.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = db.exec(statement).all()
    # return UsersPublic(data=[convert_user_to_public(u) for u in users], count=count) #
    return UsersPublic.from_orm_list(users, count)

@router.post("/users", response_model=UserPublic, status_code=status.HTTP_201_CREATED, tags=["user"])
def create_user(db: SessionDep,
    new_user: CheckUserExists
    # current_user: User = Depends(deps.get_current_user(required_roles=[IRoleEnum.admin]))
)->UserPublic:
    user = crud.user.create(obj_in=new_user, db_session=db)
    return UserPublic.from_orm(user)

@router.put("/user/password", response_model=UserPublic, tags=["user"])
def change_password(
    body: UpdatePassword,
    db: SessionDep,
    current_user: User = Depends(get_current_user)
) -> UserPublic:
    updated_user = crud.user.change_password(
        db_session=db,
        user=current_user,
        current_password=body.current_password,
        new_password=body.new_password
    )
    return UserPublic.from_orm(updated_user)

@router.patch("/user", tags=["user"])
def update_user(
    db: SessionDep,
    user: UserUpdate,
    current_user: User = Depends(get_current_user)
)->UserPublic:
    """
    Update user
    """
    updated_user = crud.user.update(db_session=db, obj_current=current_user, obj_new=user)
    return UserPublic.from_orm(updated_user)

@router.patch("/user/idcard", tags=["user"])
def update_user_idcard(
    db: SessionDep,
    idcard_update: IDCardInfoUpdate,
    current_user: User = Depends(get_current_user)
) -> IDCardInfo:
    id_card_info = crud.id_card_info.update(db_session=db, obj_current=current_user.id_card_info, obj_new=idcard_update) # type: ignore
    return id_card_info

@router.patch("/user/platform", tags=["user"])
def update_user_platform(
    db: SessionDep,
    platform_update: UserPlatformInfoUpdate,
    current_user: User = Depends(get_current_user)
) -> UserPlatformInfoPublic:
    print(f"update_user_platform:: input: {platform_update}")
    platform_info = crud.user_platform_info.update_with_favorite_content(db_session=db, obj_current=current_user.platform_info, obj_new=platform_update) # type: ignore
    return UserPlatformInfoPublic.from_orm(platform_info)

class UserOrTeamFollowMeta(BaseModel):
    id: int
    name: str
    nickname: str
    image: str
    email: str
    is_following: bool # 表示当前用户是否关注了目标用户
    is_followed: bool # 表示目标用户是否关注了当前用户
class UserOrTeamFollowMetaList(BaseModel):
    count: int
    data: list[UserOrTeamFollowMeta]

@router.get(
    "/{target_name}/followers",
    tags=["follow"], 
    summary="返回 name 的粉丝列表, 携带关注消息"
)
def read_target_name_followers(
    target_name: str, 
    db: SessionDep,
    current_user: User = Depends(get_current_user)
) -> UserOrTeamFollowMetaList:
    """
    - 需要携带 access_token
    - 粉丝列表: 目前不包括团队,因为团队只能被关注
    - is_following: 表示当前用户是否关注了目标用户
    - is_followed: 表示目标用户是否关注了当前用户
    """
    target_user = crud.user.get_by_name(db_session=db, name=target_name)
    
    statement_meta = select(User.id, User.name, User.nickname, User.image, User.email).join(LinkUserFollow, User.id == LinkUserFollow.follower_id).where(LinkUserFollow.followed_id == target_user.id)
    followers_meta = db.exec(statement_meta).all() # 拿到所有的粉丝
    print(f"followers_meta: {followers_meta}")
    
    # statement = select(User).join(LinkUserFollow, User.id == LinkUserFollow.follower_id).where(LinkUserFollow.followed_id == target_user.id)
    # followers = db.exec(statement).all() # 拿到所有的粉丝
    # pprint(f"followers: {followers}")
    
    followers_data = []
    for follower in followers_meta:
        # 关注发起者id==当前用户id, 被关注者id==列表中item id
        is_following = db.exec(select(LinkUserFollow).where(LinkUserFollow.follower_id == current_user.id).where(LinkUserFollow.followed_id == follower.id)).first()
        is_following = db.exec(select(LinkUserFollow).where(LinkUserFollow.follower_id == current_user.id)).first()
        is_followed = db.exec(select(LinkUserFollow).where(LinkUserFollow.follower_id == follower.id).where(LinkUserFollow.followed_id == current_user.id)).first()
        followers_data.append(UserOrTeamFollowMeta(
            id=follower.id, name=follower.name, nickname=follower.nickname, image=follower.image, email=follower.email,
            is_following=bool(is_following), is_followed=bool(is_followed)
        ))
    print(f"followers_data: {followers_data}")
    return UserOrTeamFollowMetaList(count=len(followers_data), data=followers_data)

@router.get("/{target_name}/following", tags=["follow"], summary="返回 name 的关注列表, 携带关注消息")
def read_target_name_following(target_name: str, db: SessionDep,
    current_user: User = Depends(get_current_user)
    )->UserOrTeamFollowMetaList:
    """
    - 需要携带 access_token
    - 关注列表: 目前不包括团队,因为团队只能被关注
    - is_following: 表示当前用户是否关注了目标用户
    - is_followed: 表示目标用户是否关注了当前用户
    """
    target_user = crud.user.get_by_name(db_session=db, name=target_name)
    
    statement_meta = select(User.id, User.name, User.nickname, User.image, User.email).join(LinkUserFollow, User.id == LinkUserFollow.followed_id).where(LinkUserFollow.follower_id == target_user.id)
    following_meta = db.exec(statement_meta).all() # 拿到所有的关注
    print(f"following_meta: {following_meta}")
    
    following_data = []
    for follower in following_meta:
        # 关注发起者id==当前用户id, 被关注者id==列表中item id
        is_following = db.exec(select(LinkUserFollow).where(LinkUserFollow.follower_id == current_user.id).where(LinkUserFollow.followed_id == follower.id)).first()
        is_following = db.exec(select(LinkUserFollow).where(LinkUserFollow.follower_id == current_user.id)).first()
        is_followed = db.exec(select(LinkUserFollow).where(LinkUserFollow.follower_id == follower.id).where(LinkUserFollow.followed_id == current_user.id)).first()
        following_data.append(UserOrTeamFollowMeta(
            id=follower.id, name=follower.name, nickname=follower.nickname, image=follower.image, email=follower.email,
            is_following=bool(is_following), is_followed=bool(is_followed)
        ))
    print(f"following_data: {following_data}")
    return UserOrTeamFollowMetaList(count=len(following_data), data=following_data)

@router.get("/user/is_following/{target_user_id}", tags=["follow"])
def is_following_user(target_user_id: int, db: SessionDep, current_user: User = Depends(get_current_user))-> LinkUserFollow|None :
    followed_user = db.get(User, target_user_id)
    if not followed_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    link_user_follow = db.exec(select(LinkUserFollow).where(LinkUserFollow.follower_id == current_user.id).where(LinkUserFollow.followed_id == target_user_id)).first()
    return link_user_follow

@router.post("/user/follow/{target_user_id}", tags=["follow"],)
def follow_user(target_user_id: int, db: SessionDep, current_user: User = Depends(get_current_user))->User:
    """
    关注一个用户, with token and target_user_id
    """
    if target_user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Following/Unfollowing self not allowed!")
    followed_user = db.get(User, target_user_id)
    if not followed_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    link_user_follow = db.exec(select(LinkUserFollow).where(LinkUserFollow.follower_id == current_user.id).where(LinkUserFollow.followed_id == target_user_id)).first()
    if link_user_follow:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"current user({current_user.name}) has already followed the target user")
    followed_user = crud.link_user_follow.follow(follower=current_user, followed=followed_user, db_session=db)
    return followed_user

@router.post("/{name}/follow", tags=["follow"],summary="关注 name, 需要携带 access_token, 响应: 新的目标用户的信息",)
def follow_user_by_name(name: str, db: SessionDep, current_user: User = Depends(get_current_user))->User:
    """
    TODO:
    - 刚刚发现返回了一个 空 {}
    """
    if name == current_user.name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Following/Unfollowing self not allowed!")
    followed_user = crud.user.get_by_name(db_session=db, name=name)
    if not followed_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    link_user_follow = db.exec(select(LinkUserFollow).where(LinkUserFollow.follower_id == current_user.id).where(LinkUserFollow.followed_id == followed_user.id)).first()
    if link_user_follow:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"current user({current_user.name}) has already followed the target user")
    
    followed_user = crud.link_user_follow.follow(follower=current_user, followed=followed_user, db_session=db)
    return followed_user

@router.delete("/user/follow/{target_user_id}", tags=["follow"])
def unfollow_user(target_user_id: int, db: SessionDep, current_user: User = Depends(get_current_user))->User:
    followed_user = db.get(User, target_user_id)
    if not followed_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    followed_user =crud.link_user_follow.unfollow(follower=current_user, followed=followed_user, db_session=db)
    return followed_user

