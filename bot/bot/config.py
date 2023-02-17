from pydantic import BaseSettings, HttpUrl

class Settings(BaseSettings):
    BACKEND_HOST: HttpUrl
    BOT_TOKEN: str

    class Config:
        env_file: str = ".env"

settings = Settings()