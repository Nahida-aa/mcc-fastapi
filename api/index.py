import os
import sys

from sqladmin import Admin, ModelView

from server.models import User, UserPlatformInfo, Tag
from server.models.links_model import LinkUserPlatformInfoTag

# import uvicorn

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
print(BASE_PATH)

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from server.lib.database import create_db_and_tables
# from api.routes.security import route as security_route
# from api.routes.user import route as user_route
from server.lib.database import  engine
from api import user as user_api

# from api.apis.v1.api import api_router as api_router_v1



app = FastAPI(docs_url="/api/py/docs",redoc_url="/api/py/redoc", openapi_url="/api/py/openapi.json")

origins = [
    "https://127.0.0.1:3000",
    "https://127.0.0.1",
    "https://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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

app.include_router(user_api.router)

admin = Admin(app, engine)
class UserAdmin(ModelView, model=User):
    column_list = [str(User.id), User.username, str(User.is_active), str(User.is_superuser)]
class UserPlatformInfoAdmin(ModelView, model=UserPlatformInfo):
    column_list = [str(UserPlatformInfo.id)]
class TagAdmin(ModelView, model=Tag):
    column_list = [str(Tag.id), Tag.name, Tag.description]
class LinkUserPlatformInfoTagAdmin(ModelView, model=LinkUserPlatformInfoTag):
    column_list = [str(LinkUserPlatformInfoTag.user_platform_info_id), str(LinkUserPlatformInfoTag.tag_id)]
admin.add_view(UserAdmin)
admin.add_view(UserPlatformInfoAdmin)
admin.add_view(TagAdmin)
admin.add_view(LinkUserPlatformInfoTagAdmin)