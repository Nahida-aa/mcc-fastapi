import os
import secrets
import sys

import jwt
from sqladmin import Admin, ModelView

from server import crud
from server.core.security import create_access_token, create_refresh_token, decode_token
from server.models import User, UserPlatformInfo, Tag
from server.models.links_model import LinkUserPlatformInfoTag
from server.models.security_model import Token, TokenWithUser
from server.schemas.user_schema import UserPublic

# import uvicorn

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
print(BASE_PATH)

from fastapi import Body, Cookie, Depends, FastAPI, Form, HTTPException, Response, status
from pydantic import BaseModel
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from server.lib.database import create_db_and_tables
from server.lib.database import  engine
# from api import user as user_api
from server.core.config import settings
from server.deps import SessionDep, get_db
from server.deps.user_deps import CheckUserExists
# from api.apis.v1.api import api_router as api_router_v1



app = FastAPI(docs_url="/api/py/docs",redoc_url="/api/py/redoc", openapi_url="/api/py/openapi.json")

origins = [
    "https://127.0.0.1:3000",
    "http://127.0.0.1:3000",
    "https://127.0.0.1",
    "https://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/api/py/env")
# def test_env():
#     return {"message": settings.ENCRYPT_KEY}
@app.post("/api/py/token")
def get_scopes_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    OAuth2 compatible token with scopes : 获取访问令牌, 包含权限范围
    """
    with Session(engine) as db:
        user = crud.user.authenticate_user(name=form_data.name, password=form_data.password, db_session=db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"name": user.name, "scopes": form_data.scopes}
    )
    refresh_token = create_refresh_token(data={"name": user.name, "scopes": form_data.scopes})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str
@app.post("/api/py/refresh-token")
def refresh_token(refresh_token: str) -> RefreshTokenResponse:
    """
    Refresh access token using refresh token : 刷新访问令牌
    """
    try:
        payload = decode_token(refresh_token)
        user_id = payload.get("id")
        name = payload.get("name")
        if user_id is None or name is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        new_access_token = create_access_token(data={"name": name})
        return RefreshTokenResponse(access_token=new_access_token, token_type="bearer")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
@app.get("/api/py/auth/csrf")
def get_csrf_token(response: Response):
    """
    Generate and return a CSRF token
    """
    csrf_token = secrets.token_urlsafe(32)
    response.set_cookie(key="csrf_token", value=csrf_token, httponly=True, samesite="strict")
    return {"csrfToken": csrf_token}

@app.post("/api/py/login")
def login(response: Response, db: SessionDep,
          name: str = Body(...),
          password: str = Body(...)
)->TokenWithUser:
    """
    User login, get an access token and refresh token
    """
    user = crud.user.authenticate_user(name=name, password=password, db_session=db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"id": user.id,"name": user.name, "image":user.image, "email":user.email, "nickname":user.nickname})
    refresh_token = create_refresh_token(data={"id": user.id,"name": user.name, "image":user.image, "email":user.email, "nickname":user.nickname})
    
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, samesite="strict")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60, samesite="strict")
    
    return TokenWithUser(access_token=access_token, refresh_token=refresh_token, token_type="bearer", user=UserPublic.from_orm(user))

class JsonBody(BaseModel):
    name: str
    password: str
@app.post("/api/py/auth/signin")
def signin(response: Response, db: SessionDep,
            data: Annotated[JsonBody, Form(...)]
)->TokenWithUser:
    """
    User sign in, get an access token and refresh token
    """
    print(f"signin: {data}")
    user = crud.user.authenticate_user(name=data.name, password=data.password, db_session=db)
    print(f"signin: {user}")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"id": user.id,"name": user.name, "image":user.image, "email":user.email, "nickname":user.nickname})
    refresh_token = create_refresh_token(data={"id": user.id,"name": user.name, "image":user.image, "email":user.email, "nickname":user.nickname})
    
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, samesite="strict")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60, samesite="strict")
    
    return TokenWithUser(access_token=access_token, refresh_token=refresh_token, token_type="bearer", user=UserPublic.from_orm(user))

class SignOutBody(BaseModel):
    csrfToken: str
    redirectTo: str | None = None
class SignOutCookies(BaseModel):
    csrf_token: str

@app.post("/api/py/auth/signout")
def signout(response: Response, db: SessionDep,
    cookies: Annotated[SignOutCookies, Cookie()],
    form_data: Annotated[SignOutBody, Form(...)],
):
    if form_data.csrfToken != cookies.csrf_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid CSRF token")
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"redirectTo": form_data.redirectTo}

@app.post("/api/py/register")
def register(db: SessionDep, new_user: CheckUserExists)->TokenWithUser:
    user = crud.user.create(obj_in=new_user, db_session=db)
    access_token = create_access_token(data={"id": user.id,"name": user.name, "image":user.image, "email":user.email, "nickname":user.nickname})
    refresh_token = create_refresh_token(data={"id": user.id,"name": user.name, "image":user.image, "email":user.email, "nickname":user.nickname})
    return TokenWithUser(access_token=access_token, refresh_token=refresh_token, token_type="bearer", user=UserPublic.from_orm(user))
# def select_users():
#     # with Session(engine) as session:
#     #     users = session.exec(select(User)).all()
#     #     print(f"All users: {users}")
#     pass
# def main():
#     create_db_and_tables()
#     select_users()

# if __name__ == "__main__":
#     main()
#     uvicorn.run("main:app", port=5000, log_level="info")

# Add Routers
# app.include_router(api_router_v1, prefix=settings.API_V1_STR)
# app.include_router(api_router_v1, prefix="/api/v1/py")

# from io import BytesIO
# from typing import Annotated
# from uuid import UUID
from pprint import pprint
from server.utils.exceptions import (
    # IdNotFoundException,
    SelfFollowedException,
    # UserFollowedException,
    # UserNotFollowedException,
    # UserSelfDeleteException,
)
# # from app import crud
# # from app.api import deps
# from app.deps import user_deps
# from app.models import User, UserFollow
# from app.models.role_model import Role
# from app.utils.minio_client import MinioClient
# from app.utils.resize_image import modify_image
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
from server.core.security import create_access_token, create_refresh_token, get_password_hash
from server.deps.security_dep import get_current_user,  CurrentUser
from server.models.links_model import LinkUserFollow
from server.models.user_model import IDCardInfo,  User,  UserPlatformInfo
from server.schemas.user_schema import IDCardInfoUpdate, UpdatePassword, UserCreate, UserPlatformInfoPublic, UserPlatformInfoUpdate, UserPublic, UserUpdate, UsersPublic
from server.models.security_model import Token, TokenWithUser
from server.deps import SessionDep, user_deps
from server.deps.user_deps import CheckUserExists
# from app.schemas.media_schema import IMediaCreate
# from app.schemas.response_schema import (
#     IDeleteResponseBase,
#     IGetResponseBase,
#     IGetResponsePaginated,
#     IPostResponseBase,
#     IPutResponseBase,
#     create_response,
# )
# from app.schemas.role_schema import IRoleEnum
# from app.schemas.user_follow_schema import IUserFollowRead
# from app.schemas.user_schema import (
#     IUserCreate,
#     IUserRead,
#     IUserReadWithoutGroups,
#     IUserStatus,
# )
# from app.schemas.user_follow_schema import (
#     IUserFollowReadCommon,
# )
# from fastapi_pagination import Params #我认为不具有正规性
# from sqlmodel import and_, select, col, or_, text

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

# @router.get("/list")
# async def read_users_list(
#     params: Params = Depends(),
#     current_user: User = Depends(
#         deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
#     ),
# ) -> IGetResponsePaginated[IUserReadWithoutGroups]:
#     """
#     Retrieve users. Requires admin or manager role

#     Required roles:
#     - admin
#     - manager
#     """
#     users = await crud.user.get_multi_paginated(params=params)
#     return create_response(data=users)


# @router.get("/list/by_role_name")
# async def read_users_list_by_role_name(
#     name: str = "",
#     user_status: Annotated[
#         IUserStatus,
#         Query(
#             title="User status",
#             description="User status, It is optional. Default is active",
#         ),
#     ] = IUserStatus.active,
#     role_name: str = "",
#     params: Params = Depends(),
#     current_user: User = Depends(
#         deps.get_current_user(required_roles=[IRoleEnum.admin])
#     ),
# ) -> IGetResponsePaginated[IUserReadWithoutGroups]:
#     """
#     Retrieve users by role name and status. Requires admin role

#     Required roles:
#     - admin
#     """
#     user_status = True if user_status == IUserStatus.active else False
#     query = (
#         select(User)
#         .join(Role, User.role_id == Role.id)
#         .where(
#             and_(
#                 col(Role.name).ilike(f"%{role_name}%"),
#                 User.is_active == user_status,
#                 or_(
#                     col(User.first_name).ilike(f"%{name}%"),
#                     col(User.last_name).ilike(f"%{name}%"),
#                     text(
#                         f"""'{name}' % concat("User".last_name, ' ', "User".first_name)"""
#                     ),
#                     text(
#                         f"""'{name}' % concat("User".first_name, ' ', "User".last_name)"""
#                     ),
#                 ),
#             )
#         )
#         .order_by(User.first_name)
#     )
#     users = await crud.user.get_multi_paginated(query=query, params=params)
#     return create_response(data=users)


# @router.get("/order_by_created_at")
# async def get_user_list_order_by_created_at(
#     params: Params = Depends(),
#     current_user: User = Depends(
#         deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
#     ),
# ) -> IGetResponsePaginated[IUserReadWithoutGroups]:
#     """
#     Gets a paginated list of users ordered by created datetime

#     Required roles:
#     - admin
#     - manager
#     """
#     users = await crud.user.get_multi_paginated_ordered(
#         params=params, order_by="created_at"
#     )
#     return create_response(data=users)


# # @router.get("/following")
# # async def get_following(
# #     params: Params = Depends(),
# #     current_user: User = Depends(deps.get_current_user()),
# # ) -> IGetResponsePaginated[IUserFollowReadCommon]:
# #     """
# #     Lists the people who the authenticated user follows.
# #     """
# #     query = (
# #         select(
# #             User.id,
# #             User.first_name,
# #             User.last_name,
# #             User.follower_count,
# #             User.following_count,
# #             UserFollow.is_mutual,
# #         )
# #         .join(UserFollow, User.id == UserFollow.target_user_id)
# #         .where(UserFollow.user_id == current_user.id)
# #     )
# #     users = await crud.user.get_multi_paginated(query=query, params=params)
# #     return create_response(data=users)


# @router.get(
#     "/following/{user_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     response_class=Response,
# )
# async def check_is_followed_by_user_id(
#     user: User = Depends(user_deps.is_valid_user),
#     current_user: User = Depends(deps.get_current_user()),
# ):
#     """
#     Check if a person is followed by the authenticated user
#     """
#     result = await crud.user_follow.get_follow_by_user_id_and_target_user_id(
#         user_id=user.id, target_user_id=current_user.id
#     )
#     if not result:
#         raise UserNotFollowedException(user_name=user.last_name)

#     raise UserFollowedException(target_user_name=user.last_name)


# # @router.get("/followers")
# # async def get_followers(
# #     params: Params = Depends(),
# #     current_user: User = Depends(deps.get_current_user()),
# # ) -> IGetResponsePaginated[IUserFollowReadCommon]:
# #     """
# #     Lists the people following the authenticated user.
# #     """
# #     query = (
# #         select(
# #             User.id,
# #             User.first_name,
# #             User.last_name,
# #             User.follower_count,
# #             User.following_count,
# #             UserFollow.is_mutual,
# #         )
# #         .join(UserFollow, User.id == UserFollow.user_id)
# #         .where(UserFollow.target_user_id == current_user.id)
# #     )
# #     users = await crud.user.get_multi_paginated(params=params, query=query)
# #     return create_response(data=users)


# # @router.get("/{user_id}/followers")
# # async def get_user_followed_by_user_id(
# #     user_id: UUID = Depends(user_deps.is_valid_user_id),
# #     params: Params = Depends(),
# #     current_user: User = Depends(deps.get_current_user()),
# # ) -> IGetResponsePaginated[IUserFollowReadCommon]:
# #     """
# #     Lists the people following the specified user.
# #     """
# #     query = (
# #         select(
# #             User.id,
# #             User.first_name,
# #             User.last_name,
# #             User.follower_count,
# #             User.following_count,
# #             UserFollow.is_mutual,
# #         )
# #         .join(UserFollow, User.id == UserFollow.user_id)
# #         .where(UserFollow.target_user_id == user_id)
# #     )
# #     users = await crud.user.get_multi_paginated(params=params, query=query)
# #     return create_response(data=users)


# # @router.get("/{user_id}/following")
# # async def get_user_following_by_user_id(
# #     user_id: UUID = Depends(user_deps.is_valid_user_id),
# #     params: Params = Depends(),
# #     current_user: User = Depends(deps.get_current_user()),
# # ) -> IGetResponsePaginated[IUserFollowReadCommon]:
# #     """
# #     Lists the people who the specified user follows.
# #     """
# #     query = (
# #         select(
# #             User.id,
# #             User.first_name,
# #             User.last_name,
# #             User.follower_count,
# #             User.following_count,
# #             UserFollow.is_mutual,
# #         )
# #         .join(UserFollow, User.id == UserFollow.target_user_id)
# #         .where(UserFollow.user_id == user_id)
# #     )
# #     users = await crud.user.get_multi_paginated(query=query, params=params)
# #     return create_response(data=users)

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

@router.get("/{target_name}/followers", tags=["follow"], summary="返回 name 的粉丝列表, 携带关注消息")
def read_target_name_followers(target_name: str, db: SessionDep,
    current_user: User = Depends(get_current_user)
    )->UserOrTeamFollowMetaList:
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
    
    statement = select(User).join(LinkUserFollow, User.id == LinkUserFollow.follower_id).where(LinkUserFollow.followed_id == target_user.id)
    followers = db.exec(statement).all() # 拿到所有的粉丝
    pprint(f"followers: {followers}")
    
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

# @router.delete("/following/{target_user_id}")
# async def unfollowing_a_user_by_id(
#     target_user_id: UUID,
#     current_user: User = Depends(deps.get_current_user()),
# ) -> IDeleteResponseBase[IUserFollowRead]:
#     """
#     Unfollowing a user
#     """
#     if target_user_id == current_user.id:
#         raise SelfFollowedException()
#     target_user = await crud.user.get(id=target_user_id)
#     if not target_user:
#         raise IdNotFoundException(User, id=target_user_id)

#     current_follow_user = await crud.user_follow.get_follow_by_target_user_id(
#         user_id=current_user.id, target_user_id=target_user_id
#     )

#     if not current_follow_user:
#         raise UserNotFollowedException(user_name=target_user.last_name)

#     user_follow = await crud.user_follow.unfollow_a_user_by_id(
#         user_follow_id=current_follow_user.id,
#         user=current_user,
#         target_user=target_user,
#     )
#     return create_response(data=user_follow)


# @router.get("/{user_id}")
# async def get_user_by_id(
#     user: User = Depends(user_deps.is_valid_user),
#     current_user: User = Depends(
#         deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
#     ),
# ) -> IGetResponseBase[IUserRead]:
#     """
#     Gets a user by his/her id

#     Required roles:
#     - admin
#     - manager
#     """
#     return create_response(data=user)


# @router.get("")
# async def get_my_data(
#     current_user: User = Depends(deps.get_current_user()),
# ) -> IGetResponseBase[IUserRead]:
#     """
#     Gets my user profile information
#     """
#     return create_response(data=current_user)


# @router.post("", status_code=status.HTTP_201_CREATED)
# async def create_user(
#     new_user: IUserCreate = Depends(user_deps.user_exists),
#     current_user: User = Depends(
#         deps.get_current_user(required_roles=[IRoleEnum.admin])
#     ),
# ) -> IPostResponseBase[IUserRead]:
#     """
#     Creates a new user

#     Required roles:
#     - admin
#     """
#     user = await crud.user.create_with_role(obj_in=new_user)
#     return create_response(data=user)


# @router.delete("/{user_id}")
# async def remove_user(
#     user_id: UUID = Depends(user_deps.is_valid_user_id),
#     current_user: User = Depends(
#         deps.get_current_user(required_roles=[IRoleEnum.admin])
#     ),
# ) -> IDeleteResponseBase[IUserRead]:
#     """
#     Deletes a user by his/her id

#     Required roles:
#     - admin
#     """
#     if current_user.id == user_id:
#         raise UserSelfDeleteException()

#     user = await crud.user.remove(id=user_id)
#     return create_response(data=user, message="User removed")


# @router.post("/image")
# async def upload_my_image(
#     title: str | None = Body(None),
#     description: str | None = Body(None),
#     image_file: UploadFile = File(...),
#     current_user: User = Depends(deps.get_current_user()),
#     minio_client: MinioClient = Depends(deps.minio_auth),
# ) -> IPostResponseBase[IUserRead]:
#     """
#     Uploads a user image
#     """
#     try:
#         image_modified = modify_image(BytesIO(image_file.file.read()))
#         data_file = minio_client.put_object(
#             file_name=image_file.filename,
#             file_data=BytesIO(image_modified.file_data),
#             content_type=image_file.content_type,
#         )
#         print("data_file", data_file)
#         media = IMediaCreate(
#             title=title, description=description, path=data_file.file_name
#         )
#         user = await crud.user.update_photo(
#             user=current_user,
#             image=media,
#             heigth=image_modified.height,
#             width=image_modified.width,
#             file_format=image_modified.file_format,
#         )
#         return create_response(data=user)
#     except Exception as e:
#         print(e)
#         return Response("Internal server error", status_code=500)


# @router.post("/{user_id}/image")
# async def upload_user_image(
#     user: User = Depends(user_deps.is_valid_user),
#     title: str | None = Body(None),
#     description: str | None = Body(None),
#     image_file: UploadFile = File(...),
#     current_user: User = Depends(
#         deps.get_current_user(required_roles=[IRoleEnum.admin])
#     ),
#     minio_client: MinioClient = Depends(deps.minio_auth),
# ) -> IPostResponseBase[IUserRead]:
#     """
#     Uploads a user image by his/her id

#     Required roles:
#     - admin
#     """
#     try:
#         image_modified = modify_image(BytesIO(image_file.file.read()))
#         data_file = minio_client.put_object(
#             file_name=image_file.filename,
#             file_data=BytesIO(image_modified.file_data),
#             content_type=image_file.content_type,
#         )
#         media = IMediaCreate(
#             title=title, description=description, path=data_file.file_name
#         )
#         user = await crud.user.update_photo(
#             user=user,
#             image=media,
#             heigth=image_modified.height,
#             width=image_modified.width,
#             file_format=image_modified.file_format,
#         )
#         return create_response(data=user)
#     except Exception as e:
#         print(e)
#         return Response("Internal server error", status_code=500)
# app.include_router(user_api.router)
app.include_router(router)

admin = Admin(app, engine, base_url="/api/py/admin")
class UserAdmin(ModelView, model=User):
    column_list = [str(User.id), User.name, str(User.is_active), str(User.is_superuser)]
class UserPlatformInfoAdmin(ModelView, model=UserPlatformInfo):
    column_list = [str(UserPlatformInfo.id)]
class TagAdmin(ModelView, model=Tag):
    column_list = [str(Tag.id), Tag.name, Tag.description]
class LinkUserPlatformInfoTagAdmin(ModelView, model=LinkUserPlatformInfoTag):
    column_list = [str(LinkUserPlatformInfoTag.user_platform_info_id), str(LinkUserPlatformInfoTag.tag_id)]
admin.add_view(UserAdmin)
admin.add_view(UserPlatformInfoAdmin)
admin.add_view(TagAdmin)
admin.add_view(LinkUserPlatformInfoTagAdmin)