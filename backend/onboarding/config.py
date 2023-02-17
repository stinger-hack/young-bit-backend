from pathlib import Path
from typing import Any, Mapping, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 6432
    POSTGRES_DATABASE: str
    POSTGRES_TEST_DATABASE: str = ""
    DATABASE_URL: PostgresDsn = ""
    TEST_DATABASE_URL: PostgresDsn | str = ""
    ALEMBIC_DATABASE_URL: PostgresDsn = ""

    CELERY_BROKER_URL: str = ""
    CELERY_BACKEND_URL: str = ""

    SERVER_PORT: int = 8000
    SERVER_HOST: str = "0.0.0.0"

    AUTH_ALGORITHM: str = "RS256"
    AUTH_EXPIRES_SECONDS: int = 3600

    AUTH_PUBLIC_KEY: Path = ""
    AUTH_PRIVATE_KEY: Path = ""
    AUTH_PUBLIC_KEY_DATA: str = None
    AUTH_PRIVATE_KEY_DATA: str = None

    S3_ENDPOINT_URL = ""
    S3_AWS_ACCESS_KEY_ID = ""
    S3_AWS_SECRET_ACCESS_KEY = ""
    BUCKET_NAME = ""
    REGION_NAME = ""

    class Config:
        env_file = ".env"

    @validator("DATABASE_URL", pre=True)
    def assemble_postgres_db_url(cls, v: Optional[str], values: Mapping[str, Any]) -> str:
        if v and isinstance(v, str):
            return v

        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                user=values["POSTGRES_USER"],
                password=values["POSTGRES_PASSWORD"],
                host=values["POSTGRES_HOST"],
                port=str(values["POSTGRES_PORT"]),
                path=f'/{values["POSTGRES_DATABASE"]}',
            )
        )

    @validator("AUTH_PRIVATE_KEY_DATA", pre=True)
    def prepare_private_file(cls, v: Optional[str], values: Mapping[str, Any]):
        if v and isinstance(v, str):
            return v
        result = open(values["AUTH_PRIVATE_KEY"], mode="r").read()
        return result

    @validator("AUTH_PUBLIC_KEY_DATA", pre=True)
    def prepare_public_file(cls, v: Optional[str], values: Mapping[str, Any]):
        if v and isinstance(v, str):
            return v
        result = open(values["AUTH_PUBLIC_KEY"], mode="r").read()
        return result

    @validator("ALEMBIC_DATABASE_URL", pre=True)
    def assemble_alembic_database_url(cls, v: Optional[str], values: Mapping[str, Any]) -> str:
        if v and isinstance(v, str):
            return v

        return str(
            PostgresDsn.build(
                scheme="postgresql",
                user=values["POSTGRES_USER"],
                password=values["POSTGRES_PASSWORD"],
                host=values["POSTGRES_HOST"],
                port=str(values["POSTGRES_PORT"]),
                path=f'/{values["POSTGRES_DATABASE"]}',
            )
        )


settings = Settings()
