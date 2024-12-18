import os
import secrets

from dotenv import load_dotenv

load_dotenv()

class Settings():
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 100  # 100 days

    SECRET_KEY: str = os.getenv("SECRET_KEY") or secrets.token_urlsafe(32)
    ENCRYPT_KEY: str = os.getenv("ENCRYPT_KEY") or secrets.token_urlsafe(32)

settings = Settings() 