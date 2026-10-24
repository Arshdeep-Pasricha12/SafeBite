import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

_BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
_DEFAULT_DB_FILE = _BASE_DIR / "database" / "safebite.db"
_FALLBACK_URL = f"sqlite:///{_DEFAULT_DB_FILE.as_posix()}" if _DEFAULT_DB_FILE.exists() else "sqlite:///database/safebite.db"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secret_key_safebite_1234567890")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database - SINGLE SOURCE OF TRUTH
    DATABASE_URL: str = os.getenv("DATABASE_URL", _FALLBACK_URL)

settings = Settings()
