from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi import Depends, HTTPException, Request, Response, Security, status, Cookie
import jwt
from pydantic import BaseModel, ValidationError
from server.core.config import settings

from server import crud
from server.core.security import create_access_token, decode_token
from server.models.security_model import TokenData
from server.deps import SessionDep


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "read_user": "Read self user",
        "write_user": "Write self user",
        "read_users": "Read users",
        "write_users": "Write users",
        "read_proj": "Read 自己的proj(包括私有)",
        "write_team": "Write 团队",
        "write_team_proj": "Write 团队的proj",
    },
    auto_error=False # 不自动抛出异常 而是返回None, 以便后续处理
) # 从请求头拿Authorization: Bearer token, else 401

class Cookies(BaseModel):
    access_token: str|None = None
    refresh_token: str|None = None
async def get_current_user(db_session: SessionDep, security_scopes: SecurityScopes, token: Annotated[str|None, Depends(oauth2_scheme)],
    cookies: Annotated[Cookies, Cookie()],
    response: Response
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        if token is None:
            print(f"获得当前用户::access_token: {cookies.access_token}")
            token = cookies.access_token
        if token is None and cookies.refresh_token is not None:
            print(f"获得当前用户::refresh_token: {cookies.refresh_token}")
            payload = decode_token(cookies.refresh_token)
            username = payload.get("username")
            if username is None:
                raise credentials_exception
            token = create_access_token(data={"username": username})
            response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,
                max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # 转换为秒
                samesite="strict"
            )
        print(f"获得当前用户::token: {token}")
        payload = decode_token(token)
        print(f"获得当前用户::payload: {payload}")
        username = payload.get("username")
        print(f"获得当前用户::username: {username}")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (jwt.InvalidTokenError, ValidationError):
        raise credentials_exception
    user = crud.user.get_by_username(username=token_data.username, db_session=db_session)
    print(f"获得当前用户::user: {user}")
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user

# CurrentUser = Annotated[Security(get_current_user), Depends(oauth2_scheme)]