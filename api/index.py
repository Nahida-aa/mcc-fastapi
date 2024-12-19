import os
import secrets
import sys

import jwt

from server import crud
from server.core.security import create_access_token, create_refresh_token, decode_token
# from server.models import User, UserPlatformInfo, Tag
# from server.models.links_model import LinkUserPlatformInfoTag
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
# from server.lib.database import create_db_and_tables
from server.lib.database import  engine
from api import user as user_api
from server.core.config import settings
from server.deps import SessionDep, get_db
from server.deps.user_deps import CheckUserExists
# from api.apis.v1.api import api_router as api_router_v1

# app = FastAPI(docs_url="/api/py/docs",redoc_url="/api/py/redoc", openapi_url="/api/py/openapi.json")
app = FastAPI(docs_url="/",redoc_url="/redoc", openapi_url="/api/py/openapi.json")

origins = [
    "https://127.0.0.1:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://127.0.0.1",
    "https://127.0.0.1:8080",
    "https://mcc.Nahida-aa.us.kg",
    "mcc-next.vercel.app",
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
        user = decode_token(refresh_token)
        user_id = user.get("id")
        name = user.get("name")
        if user_id is None or name is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        new_access_token = create_access_token(data={"id": user.id,"name": user.name, "image":user.image, "email":user.email, "nickname":user.nickname})
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
    response.set_cookie(key="csrf_token", value=csrf_token, httponly=True, samesite="lax ")
    return {"csrfToken": csrf_token}

# @app.post("/api/py/login")
# def login(response: Response, db: SessionDep,
#           name: str = Body(...),
#           password: str = Body(...)
# )->TokenWithUser:
#     """
#     User login, get an access token and refresh token
#     """
#     user = crud.user.authenticate_user(name=name, password=password, db_session=db)
    
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect name or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = create_access_token(data={"id": user.id,"name": user.name, "image":user.image, "email":user.email, "nickname":user.nickname})
#     refresh_token = create_refresh_token(data={"id": user.id,"name": user.name, "image":user.image, "email":user.email, "nickname":user.nickname})
    
#     response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, samesite="strict")
#     response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60, samesite="strict")
    
#     return TokenWithUser(access_token=access_token, refresh_token=refresh_token, token_type="bearer", user=UserPublic.from_orm(user))

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


app.include_router(user_api.router)