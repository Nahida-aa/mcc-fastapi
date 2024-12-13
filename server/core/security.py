from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from passlib.context import CryptContext
from server.core.config import settings

SECRET_KEY = "dd60e1668ffb6ea94d9c30dce6fe42fa1a6cb1ae9f0f71f05860ecd1a4fc9cd6"
JWT_ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        jwt=token,
        key=settings.ENCRYPT_KEY,
        algorithms=[JWT_ALGORITHM],
    )