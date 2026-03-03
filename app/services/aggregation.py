from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func

from core.logger import logger
from models.raw_product import RawProduct


class AggregationService:
    BATCH_SIZE = 500

    async def save_to_db(
        self,
        session,
        products: list[dict],
        shop_id: int,
    ) -> int:
        logger.debug(f"Saving {len(products)} products to database")

        if not products:
            return 0

        unique_products: dict[tuple[int, str], dict] = {}
        skipped_without_id = 0

        for product in products:
            source_id = product.get("variant_id") or product.get("product_id")
            if source_id is None:
                skipped_without_id += 1
                continue

            key = (shop_id, str(source_id))
            unique_products[key] = product

        if skipped_without_id:
            logger.warning(f"Skipped {skipped_without_id} products without id")

        logger.info(f"Deduplicated: {len(products)} -> {len(unique_products)}")

        values = []
        for (_, external_id), product in unique_products.items():
            weight = product.get("weight_g")
            values.append(
                {
                    "shop_id": shop_id,
                    "external_id": external_id,
                    "title": (product.get("product_title") or "")[:255],
                    "raw_weight": str(weight) if weight is not None else "",
                    "raw_brand": (product.get("brand_name") or "")[:255],
                    "raw_category": "cats_food",
                }
            )

        if not values:
            return 0

        saved_count = 0
        for i in range(0, len(values), self.BATCH_SIZE):
            batch = values[i : i + self.BATCH_SIZE]
            stmt = insert(RawProduct).values(batch)
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

            try:
                await session.execute(stmt)
            except Exception:
                logger.exception(
                    f"Bulk upsert failed for batch starting at index {i}"
                )
                raise

            saved_count += len(batch)

        logger.info(f"Bulk upsert completed: {saved_count} items")
        return saved_count
