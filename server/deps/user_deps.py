from typing import Annotated
from fastapi import Depends, HTTPException, Path, status
from server.schemas.user_schema import UserCreate
from server import crud
from sqlmodel import Session, select
from server.deps import SessionDep, get_db


async def check_user_exists(new_user: UserCreate, db: SessionDep) -> UserCreate:
    user = crud.user.get_by_name(name=new_user.name, db_session=db)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    if new_user.email:
        user = crud.user.get_by_email(email=new_user.email, db_session=db)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )
    # role = await crud.role.get(id=new_user.role_id)
    # if not role:
    #     raise IdNotFoundException(Role, id=new_user.role_id)

    return new_user

CheckUserExists = Annotated[UserCreate, Depends(check_user_exists)]
