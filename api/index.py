import os
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

from fastapi import Body, Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from server.lib.database import create_db_and_tables
from server.lib.database import  engine
from api import user as user_api
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
        user = crud.user.authenticate_user(username=form_data.username, password=form_data.password, db_session=db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"username": user.username, "scopes": form_data.scopes}
    )
    refresh_token = create_refresh_token(data={"username": user.username, "scopes": form_data.scopes})
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
        username = payload.get("username")
        if user_id is None or username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        new_access_token = create_access_token(data={"username": username})
        return RefreshTokenResponse(access_token=new_access_token, token_type="bearer")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

@app.post("/api/py/login")
def login(response: Response, db: SessionDep,
          username: str = Body(...),
          password: str = Body(...)
)->TokenWithUser:
    """
    User login, get an access token and refresh token
    """
    user = crud.user.authenticate_user(username=username, password=password, db_session=db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"username": user.username})
    refresh_token = create_refresh_token(data={"username": user.username})
    
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, samesite="strict")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60, samesite="strict")
    
    return TokenWithUser(access_token=access_token, refresh_token=refresh_token, token_type="bearer", user=UserPublic.from_orm(user))

@app.post("/api/py/register")
def register(db: SessionDep, new_user: CheckUserExists)->TokenWithUser:
    user = crud.user.create(obj_in=new_user, db_session=db)
    access_token = create_access_token(data={"username": user.username})
    refresh_token = create_refresh_token(data={"username": user.username})
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

app.include_router(user_api.router)

admin = Admin(app, engine, base_url="/api/py/admin")
class UserAdmin(ModelView, model=User):
    column_list = [str(User.id), User.username, str(User.is_active), str(User.is_superuser)]
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