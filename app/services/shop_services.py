from sqlalchemy import select
from sqlaclchemy.ext.asyncio import AsyncSession
from models.shop import Shop

async def get_or_create_shop(
        session: AsyncSession,
        name: str,
        base_url: str | None = None,
) -> int:
    stmt = select(Shop).where(Shop.name == name)
    result = await session.execute(stmt)
    shop = result.scalar_one_or_none()

    if shop is None:
        shop = Shop(
            name=name,
            base_url=base_url,
        )
        session.add(shop)
        await session.flush()
    return shop.id