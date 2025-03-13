import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    ALGORITHM: str = os.getenv("ALGORITHM")
    DEBUG: bool = os.getenv("DEBUG", False)
    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET")
    GITHUB_OAUTH_URL: str = os.getenv("GITHUB_OAUTH_URL")
    GITHUB_TOKEN_URL: str = os.getenv("GITHUB_TOKEN_URL")
    GITHUB_API_URL: str = os.getenv("GITHUB_API_URL")


# Criamos uma instância única de Settings para ser importada
settings = Settings()
