
from typing import Annotated
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
import jwt
from pydantic import ValidationError

from api.routes.security.schema import TokenData, User
# from api.settings import ALGORITHM, SECRET_KEY


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

# async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
#     if security_scopes.scopes:
#         authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
#     else:
#         authenticate_value = "Bearer"
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": authenticate_value},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_scopes = payload.get("scopes", [])
#         token_data = TokenData(scopes=token_scopes, username=username)
#     except (jwt.InvalidTokenError, ValidationError):
#         raise credentials_exception
#     user = get_user_form_db_by_username(username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     for scope in security_scopes.scopes:
#         if scope not in token_data.scopes:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Not enough permissions",
#                 headers={"WWW-Authenticate": authenticate_value},
#             )
#     return user

# async def get_current_active_user(
#     current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
# ):
#     print(current_user.disabled)
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user