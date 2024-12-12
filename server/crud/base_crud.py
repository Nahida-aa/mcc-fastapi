# from fastapi_async_sqlalchemy import db

from typing import Generic, TypeVar
from sqlmodel import SQLModel, select, func
from sqlmodel import SQLModel


ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model
    # def get_db(self):
    #     return db