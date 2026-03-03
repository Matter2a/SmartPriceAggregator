from fastapi import FastAPI

from database.session import AsyncSessionLocal
from parsers.petshop import PetShopParser
from services.aggregation import AggregationService
from services.shop_services import get_or_create_shop

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
            shop_id = await get_or_create_shop(
                session=session,
                name="PetShop",
                base_url="https://www.petshop.ru",
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
    }
