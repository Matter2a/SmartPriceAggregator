from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from parsers.petshop import PetShopParser
from services.aggregation import AggregationService
from database.session import AsyncSessionLocal
from models.shop import Shop

app = FastAPI(title="Smart Price Aggregator")

@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/parse/petshop")
async def parse_petshop():
    parser = PetShopParser()
    data = await parser.run()

    if not data:
        return {"parsed": 0, "saved": 0}

    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = select(Shop).where(Shop.name == "PetShop")
            result = await session.execute(stmt)
            shop = result.scalar_one_or_none()

            created = False

            if shop is None:
                shop = Shop(
                    name="PetShop",
                    base_url="https://www.petshop.ru"
                )
                session.add(shop)
                try:
                    await session.flush()
                    created = True
                except Exception as e:
                    await session.rollback()
                    raise HTTPException(
                        status_code=500,
                        detail=f"Не удалось создать магазин PetShop: {str(e)}"
                    )


            shop_id = shop.id
            if shop_id is None:
                raise HTTPException(
                    status_code=500,
                    detail="Не удалось получить id магазина PetShop",
                )

            services = AggregationService()
            saved_count = await services.save_to_db(
                session=session,
                products=data,
                shop_id=shop_id,
            )

    return {
        "parsed": len(data),
        "saved": saved_count,          
        "shop_id": shop_id,
        "shop_created": created       
    }

# Нормализовать данные normalization/text.py normalization/weight.py
