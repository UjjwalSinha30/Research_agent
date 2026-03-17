# backend/app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Celery
    CELERY_BROKER_URL: str = ""     # fallback to REDIS_URL if empty
    CELERY_RESULT_BACKEND: str = "" # fallback to REDIS_URL if empty

    class Config:
        env_file = ".env"

settings = Settings()