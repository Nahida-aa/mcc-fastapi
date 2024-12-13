# from fastapi_async_sqlalchemy import db

from typing import Any, Generic, TypeVar
from sqlmodel import SQLModel, Session, select, func
from sqlmodel import SQLModel


ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model
    # def get_db(self):
    #     return db
    def update(self, *, obj_current: ModelType, 
               obj_new: UpdateSchemaType | dict[str, Any] | ModelType, db_session: Session) -> ModelType:
        
        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.model_dump( 
                exclude_unset=True
            )  # This tells Pydantic to not include the values that were not sent
        for field in update_data:
            setattr(obj_current, field, update_data[field])
        
        db_session.add(obj_current)
        db_session.commit()
        db_session.refresh(obj_current)
        return obj_current