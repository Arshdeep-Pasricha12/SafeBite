import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secret_key_safebite_1234567890")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database - SINGLE SOURCE OF TRUTH
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///d:/safebite/database/safebite.db")

    class Config:
        case_sensitive = True

settings = Settings()
