import logging

from pydantic import BaseModel

logger = logging.getLogger(__file__)

from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "backend" / "auth" / "cert" / "private.pem"
    public_key_path: Path = BASE_DIR / "backend" / "auth" / "cert" / "public.pem"
    algorithm: str = "RS256"
    # access_token_expire_minutes: int = 1440
    access_token_expire_minutes: int = 1440
    refresh_token_expire_days: int = 30


class DatabaseSettings(BaseSettings):
    db_url: str = rf"sqlite+aiosqlite:///{BASE_DIR}/backend/core/db.db"
    db_echo: bool = True


class Settings(BaseSettings):
    API_PROJECT_NAME: str = "CryptoGuardian"
    Database: DatabaseSettings = DatabaseSettings()
    static_files_path: str = "frontend/static"
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
