from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi import Depends, HTTPException, Security, status
import jwt
from pydantic import ValidationError

from server import crud
from server.core.security import decode_token
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
) # 从请求头拿Authorization: Bearer token, else 401

async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)], db_session: SessionDep):
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
        payload = decode_token(token)
        username = payload.get("username")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (jwt.InvalidTokenError, ValidationError):
        raise credentials_exception
    user = crud.user.get_by_username(username=token_data.username, db_session=db_session)
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