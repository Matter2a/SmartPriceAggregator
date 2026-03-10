from sqlalchemy import select
from models.raw_product import RawProduct
from models.master_product import MasterProduct

from normalization.product_normalize import ProductNormalizer

from core.logger import logger

class NormalizationService:
    async def run(self, session):
        result = await session.execute(
            select(RawProduct)
            .where(RawProduct.is_normalized == False)
            .limit(500)
            )

        raw_products = result.scalars().all()

        logger.info(f"Loaded {len(raw_products)} raw products")

        normalized_rows = []
        
        for product in raw_products:
            weight = int(product.raw_weight) if product.raw_weight else None
            normalized = ProductNormalizer.normalize_product(
                raw_title=product.title,
                raw_brand=product.raw_brand,
                weight_grams=weight
            )
            normalized_rows.append(
                MasterProduct(
                    raw_product_id=product.id,
                    title_normalized=normalized["title_normalized"],
                    brand_normalized=normalized["brand_normalized"],
                    blocking_key=normalized["blocking_key"],
                )
            )
            product.is_normalized = True
        session.add_all(normalized_rows)
        await session.commit() 
        logger.info(f"Saved {len(normalized_rows)} normalized products")