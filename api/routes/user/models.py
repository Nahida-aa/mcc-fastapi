import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from regex import T
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime
# SQLite 不支持 JSON, 貌似 Pydantic 也不支持 JSON 类型
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship, JSON
# from api.routes.user.schemas import FavoriteContent

from sqlalchemy.orm import declared_attr
from datetime import datetime

from api.models.base_id_model import SQLModel, TimestampMixin, AutoIDModel, AutoIDNameModel, UUIDModel, UUIDNameModel


    











