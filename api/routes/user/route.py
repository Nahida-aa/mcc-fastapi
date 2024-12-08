from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from api.routes.security import verify_password, get_password_hash
from api.routes.security.depend import get_current_active_user
from api.routes.security.schema import User, UserDB
from api.sql_app.mock.user import get_user_form_db_by_username
from . import crud, models, schemas
# from api.lib.database import SessionLocal, engine
from api.lib.database import  engine
# from sqlalchemy.orm import Session


# models.Base.metadata.create_all(bind=engine)
# Dependency
def get_db():
    # db = SessionLocal()
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/api/py",
    tags=["user"],
)

@router.post("/users/", response_model=schemas.UserCreate_Out)
def create_user(user: schemas.UserCreate_In, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/projs/", response_model=schemas.Proj)
def create_item_for_user(
    user_id: int, proj: schemas.ProjCreateIn, db: Session = Depends(get_db)
):
    return crud.create_user_proj(db=db, proj=proj, user_id=user_id)
@router.get("/projs/", response_model=list[schemas.Proj])
def read_projs(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    projs = crud.get_projs(db, skip=skip, limit=limit)
    return projs

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
async def pagination_parameters(per_page: int = 20, page: int = 1):
    return {"per_page": per_page, "page": page}

class UserMeta(BaseModel):
    id: int
    username: str
    email: str | None = None

class ReadUsersOut(BaseModel):
    users: List[User]

# users = [UserDB(id=i) for i in range(10)]
# @router.get("/users")
# async def read_users(commons: Annotated[dict, Depends(common_parameters)])->list[User]:
#     return []
