from pydantic import BaseModel

from server.models.user_model import UserPublic


class TokenWithUser(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserPublic

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenData(BaseModel):
    username: str
    scopes: list[str] = []