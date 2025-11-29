from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    API_V1_STR: str = os.getenv("API_V1_STR")

    # admin

    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD")
    SESSION_SECRET: str = os.getenv("SESSION_SECRET")
    ADMIN_LOGO_URL: str = os.getenv("ADMIN_LOGO_URL", "/static/images/admin_logo.png")
    ADMIN_LOGIN_LOGO_URL: str = os.getenv(
        "ADMIN_LOGIN_LOGO_URL", "/static/images/admin_login_logo.png"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
