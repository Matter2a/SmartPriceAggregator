from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings
from sqlalchemy import text
engine = create_async_engine(settings.DATABASE_URL, echo=settings.SQL_ECHO)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def test_connect():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        print("Подключение к БД", result.scalar())
