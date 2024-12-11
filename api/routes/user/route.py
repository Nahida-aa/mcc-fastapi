from ast import mod
import json
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from api import models
from api.routes.security import verify_password, get_password_hash
# from api.routes.security.depend import get_current_active_user
# from api.routes.security.schema import 
# from . import crud, models, schemas
# from api.lib.database import SessionLocal, engine
from api.lib.database import  engine
# from sqlalchemy.orm import Session


# models.Base.metadata.create_all(bind=engine)
# Dependency
# def get_db():
#     # db = SessionLocal()
#     db = Session(engine)
#     try:
#         yield db
#     finally:
#         db.close()
def get_db():
    with Session(engine) as session:
        yield session
        
router = APIRouter(
    prefix="/api/py",
    tags=["user"],
)

@router.get("/users/", response_model=list[models.UserPublic])
def read_users(offset: int = 0, limit: int = Query(default=100, le=100), db: Session = Depends(get_db)):
    # with Session(engine) as db:
    users = db.exec(
        select(models.User)
        # .options(joinedload(models.User.id_card_info))
        # .options(joinedload(models.IDCardInfo))
        # .join(models.IDCardInfo)
        .offset(offset).limit(limit)
    ).all()
    print(f"users: {users}")
    return users

# @router.post("/users/", response_model=models.UserPublic)
# def create_user(user: models.UserCreate):
#     hashed_password = get_password_hash(user.password)
#     with Session(engine) as db:
#         db_user = models.User.model_validate(user, update={"hashed_password": hashed_password})
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
#         return db_user

# @router.post("/users/", response_model=models.UserPublic)
# def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_username(db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)



# @router.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users

# @router.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @router.post("/users/{user_id}/projs/", response_model=schemas.Proj)
# def create_item_for_user(
#     user_id: int, proj: schemas.ProjCreateIn, db: Session = Depends(get_db)
# ):
#     return crud.create_user_proj(db=db, proj=proj, user_id=user_id)
# @router.get("/projs/", response_model=list[schemas.Proj])
# def read_projs(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
#     projs = crud.get_projs(db, skip=skip, limit=limit)
#     return projs

# async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
#     return {"q": q, "skip": skip, "limit": limit}
# async def pagination_parameters(per_page: int = 20, page: int = 1):
#     return {"per_page": per_page, "page": page}

# class UserMeta(BaseModel):
#     id: int
#     username: str
#     email: str | None = None

# class ReadUsersOut(BaseModel):
#     users: List[User]

# users = [UserDB(id=i) for i in range(10)]
# @router.get("/users")
# async def read_users(commons: Annotated[dict, Depends(common_parameters)])->list[User]:
#     return []


# @router.post("/users/", response_model=schemas.UserCreate_Out)
# def create_user(user: schemas.UserCreate_In, db: Session = Depends(get_db)):
#     db_user = db.exec(select(models.User).where(models.User.username == user.username)).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user

# @router.get("/users/", response_model=List[schemas.UserCreate_Out])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = db.exec(select(models.User).offset(skip).limit(limit)).all()
#     return users

# @router.post("/teams/", response_model=schemas.UserCreate_Out)
# def create_team(team: schemas.TeamCreate_In, db: Session = Depends(get_db)):
#     db.add(team)
#     db.commit()
#     db.refresh(team)
#     return team

# @router.get("/teams/", response_model=List[schemas.UserCreate_Out])
# def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     teams = db.exec(select(models.Team).offset(skip).limit(limit)).all()
#     return teams

# @router.post("/projects/", response_model=schemas.ProjCreate_Out)
# def create_project(project: schemas.ProjectCreate_Out, db: Session = Depends(get_db)):
#     db.add(project)
#     db.commit()
#     db.refresh(project)
#     return project

# @router.get("/projects/", response_model=List[schemas.ProjectRead])
# def read_projects(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
#     projects = session.exec(select(models.Project).offset(skip).limit(limit)).all()
#     return projects

# @router.post("/resources/", response_model=schemas.ResourceRead)
# def create_resource(resource: schemas.ResourceCreate, session: Session = Depends(get_session)):
#     session.add(resource)
#     session.commit()
#     session.refresh(resource)
#     return resource

# @router.get("/resources/", response_model=List[schemas.ResourceRead])
# def read_resources(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
#     resources = session.exec(select(models.Resource).offset(skip).limit(limit)).all()
#     return resources

# @router.post("/events/", response_model=schemas.EventRead)
# def create_event(event: schemas.EventCreate, session: Session = Depends(get_session)):
#     session.add(event)
#     session.commit()
#     session.refresh(event)
#     return event

# @router.get("/events/", response_model=List[schemas.EventRead])
# def read_events(actor_type: Optional[str] = None, actor_id: Optional[int] = None, target_type: Optional[str] = None, target_id: Optional[int] = None, event_type: Optional[str] = None, skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
#     query = select(models.Event)
#     if actor_type and actor_id:
#         query = query.where(models.Event.actor_type == actor_type, models.Event.actor_id == actor_id)
#     if target_type and target_id:
#         query = query.where(models.Event.target_type == target_type, models.Event.target_id == target_id)
#     if event_type:
#         query = query.where(models.Event.event_type == event_type)
#     events = session.exec(query.offset(skip).limit(limit)).all()
#     return events