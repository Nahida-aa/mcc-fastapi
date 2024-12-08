from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None

class UserDB(User):
    id: int
    hashed_password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    scopes: list[str] = []
    
class Permission(BaseModel):
    id: int
    content_type_id: int
    name: str # Can view model_name, Can add model_name, Can change model_name, Can delete model_name
    codename: str # view_modelName, add_modelName, change_modelName, delete_modelName
class ContentType(BaseModel):
    id: int
    model: str