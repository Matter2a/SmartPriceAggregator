from fastapi import FastAPI

from database.session import AsyncSessionLocal
from parsers.petshop import PetShopParser
from services.aggregation import AggregationService
from services.shop_services import get_or_create_shop

from core.logger import logger

import time
app = FastAPI(title="Smart Price Aggregator")


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/parse/petshop")
async def parse_petshop():
    logger.info("Petshop parsing started")

    total_start = time.perf_counter()

    parser = PetShopParser()
    
    parse_start = time.perf_counter()
    data = await parser.run()
    parse_time = time.perf_counter() - parse_start
    
    logger.info(f"Parsing finished in {parse_time:.2f} seconds")
    if not data:
        logger.warning("No data parsed from PetShop")
        return {"parsed": 0, "saved": 0}

    async with AsyncSessionLocal() as session:
        async with session.begin():
            shop_id = await get_or_create_shop(
                session=session,
                name="PetShop",
                base_url="https://www.petshop.ru",
            )
            logger.info(f"Using shop_id={shop_id}")
            services = AggregationService()
            save_start = time.perf_counter()
            saved_count = await services.save_to_db(
                session=session,
                products=data,
                shop_id=shop_id,
            )
            save_time = time.perf_counter() - save_start
            logger.info(f"Saving finished in {save_time:.2f} seconds")

    total_time = time.perf_counter() - total_start
    logger.info(f"Total request finished in {total_time:.2f} seconds")
    logger.info(f"Saved {saved_count} products")
    return {
        "parsed": len(data),
        "saved": saved_count,
        "shop_id": shop_id,
    }
