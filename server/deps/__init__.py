# from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from server.lib.database import  engine

# Dependency
# def get_db():
#     # db = SessionLocal()
#     db = Session(engine)
#     try:
#         yield db
#     finally:
#         db.close()

def get_db():
    with Session(engine) as db:
        yield db
        
SessionDep = Annotated[Session, Depends(get_db)]