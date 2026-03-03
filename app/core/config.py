from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:FAZF070522@localhost:5432/smart_price"
    SQL_ECHO: bool = False
settings = Settings()
