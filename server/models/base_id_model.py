from uuid import UUID, uuid4
# from app.utils.uuid6 import uuid7
from sqlmodel import SQLModel as _SQLModel, Field
from sqlalchemy.orm import declared_attr
from datetime import datetime

# id: implements proposal uuid7 draft4
class SQLModel(_SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__
    
class TimestampMixin(SQLModel):
    updated_at: datetime | None = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})
    created_at: datetime | None = Field(default_factory=datetime.now)

class AutoIDModel(TimestampMixin):
    id: int|None = Field(default=None, primary_key=True)

class UUIDModel(TimestampMixin):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    
class BaseDBModel_Create(TimestampMixin):
    name: str = Field(index=True, unique=True)
    description: str = ""
    
class AutoIDNameModel(BaseDBModel_Create, AutoIDModel):
    pass
class UUIDNameModel(BaseDBModel_Create, UUIDModel):
    pass

class RoleMixin(TimestampMixin):
    role: str = Field(default="member")