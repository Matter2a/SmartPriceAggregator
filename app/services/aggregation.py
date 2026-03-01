from sqlalchemy.dialects.postgresql import insert
from database.session import AsyncSession
from sqlalchemy.sql import func
from models.raw_product import RawProduct


class AggregationService:
    async def save_to_db(
        self,
        session: AsyncSession,
        products: list[dict],
        shop_id: int,
    ) -> int:
        if not products:
            return 0

        saved_count = 0

        for product in products:
            stmt = insert(RawProduct).values(
                shop_id=shop_id,
                external_id=str(product.get("product_id")),
                title=(product.get("product_title") or "")[:255],
                raw_weight=str(product.get("weight_g")),
                raw_brand=(product.get("brand_name") or "")[:255],
                raw_category="cats_food",
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=["shop_id", "external_id"],
                set_={
                    "title": stmt.excluded.title,
                    "raw_weight": stmt.excluded.raw_weight,
                    "raw_brand": stmt.excluded.raw_brand,
                    "raw_category": stmt.excluded.raw_category,
                    "updated_at": func.now(),
                },
            )
            await session.execute(stmt)
            saved_count += 1

        return saved_count


