from datetime import datetime, timedelta, timezone
from fastapi import Depends, APIRouter, HTTPException, Security, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .schema import Token, User
from . import (
    # authenticate_user, 
create_access_token)
from .depend import (
    # get_current_active_user, 
    #                  get_current_user, 
                     oauth2_scheme)
from api.settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    tags=["security"],
)

# @router.post("/api/py/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user = authenticate_user(form_data.username, form_data.password)
    
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username, "scopes": form_data.scopes},
#         expires_delta=access_token_expires,
#     )
#     return Token(access_token=access_token, token_type="bearer")

# @router.get("/user")
# async def read_user(current_user: Annotated[User, Depends(get_current_active_user)]):
#     return current_user
# @router.get("/user/proj/")
# async def read_own_proj(
#     current_user: Annotated[User, Security(get_current_active_user, scopes=["read_proj"])],
# ):
#     return [{"proj_id": "Foo", "owner": current_user.username}]
# @router.get("/status/")
# async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
#     return {"status": "ok"}

@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}