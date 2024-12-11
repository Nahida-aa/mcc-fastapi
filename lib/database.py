import os
# from urllib.parse import urlparse
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
# from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()
SQLALCHEMY_DATABASE_URL = f'{os.getenv("SQLALCHEMY_DATABASE_URL")}'
# tmpPostgres = urlparse(os.getenv("SQLALCHEMY_DATABASE_URL"))
# SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg2://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?ssl=require"
# psql -U postgres # 进入数据库
# \l # 查看数据库
# CREATE DATABASE mcc;
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
#     # , connect_args={"check_same_thread": False} # 这个参数仅适用于SQLite https://fastapi.org.cn/tutorial/sql-databases/#note
# )
# # engine = create_async_engine(f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?ssl=require", echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

from sqlmodel import SQLModel, create_engine

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)