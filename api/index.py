import os
import sys

import uvicorn

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
print(BASE_PATH)

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from lib.database import create_db_and_tables
# from api.routes.security import route as security_route
# from api.routes.user import route as user_route
from lib.database import  engine

# from api.apis.v1.api import api_router as api_router_v1



app = FastAPI(docs_url="/api/py/docs",redoc_url="/api/py/redoc", openapi_url="/api/py/openapi.json")




@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}
@app.post("/api/py/helloFastApiPost")
def hello_fast_api_post():
    return {"message": "Hello from FastAPI"}

# def select_users():
#     # with Session(engine) as session:
#     #     users = session.exec(select(User)).all()
#     #     print(f"All users: {users}")
#     pass
# def main():
#     create_db_and_tables()
#     select_users()

# if __name__ == "__main__":
#     main()
#     uvicorn.run("main:app", port=5000, log_level="info")

# Add Routers
# app.include_router(api_router_v1, prefix=settings.API_V1_STR)
# app.include_router(api_router_v1, prefix="/api/v1/py")
# app.include_router(user_api.router, prefix="/api/user", tags=["user"])
# app.include_router(user_route.router)