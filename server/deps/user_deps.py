from fastapi import HTTPException, Path, status
from server.models.user_model import UserCreate
from server import crud
from sqlmodel import Session, select


async def user_exist(new_user: UserCreate, db_session: Session) -> UserCreate:
    user = crud.user.get_by_username(username=new_user.username, db_session=db_session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    # role = await crud.role.get(id=new_user.role_id)
    # if not role:
    #     raise IdNotFoundException(Role, id=new_user.role_id)

    return new_user
