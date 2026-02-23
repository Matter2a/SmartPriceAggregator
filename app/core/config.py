from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:FAZF070522@localhost:5432/LocalPy"
settings = Settings()