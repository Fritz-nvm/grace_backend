from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:superuser@localhost:5432/grace"
    SECRET_KEY: str = "ghggy88uy6r5efo[-90836234excu7u900jpj0908i989h]"
    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "Clothing Brand API"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
