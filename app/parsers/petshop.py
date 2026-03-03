import asyncio
import random

from playwright.async_api import async_playwright

from core.logger import logger


class PetShopParser:
    BASE_API = "https://www.petshop.ru/api/v4/site/catalog/products/"
    PARAMS = {
        "cityId": 21,
        "categoryId": 926,
        "orderingId": 1,
    }
    RETRIES = 3
    PAGE_DELAY_RANGE = (0.2, 0.5)
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.petshop.ru/",
    }

    async def fetch_page(self, api, page_number: int):
        params = self.PARAMS.copy()
        params["page"] = page_number
        retry_statuses = {429, 500, 502, 503, 504}

        for attempt in range(self.RETRIES):
            response = await api.get(self.BASE_API, params=params)

            if response.status == 200:
                return await response.json()

            if response.status in retry_statuses:
                await asyncio.sleep(1 + attempt)
                continue

            if response.status == 400:
                return None

            return None

        return None

    def parse_product(self, data: dict) -> list[dict]:
        if not data:
            return []

        products = data.get("products", [])
        results = []

        for product in products:
            base = {
                "product_id": product.get("currentId"),
                "product_title": product.get("title"),
                "brand_name": product.get("brandName"),
                "product_rating": product.get("rating"),
                "product_url": product.get("url"),
            }

            for variant in product.get("variants", []):
                prices = variant.get("price") or [0, 0]
                row = base.copy()
                row.update(
                    {
                        "variant_id": variant.get("id"),
                        "weight_g": variant.get("weight", 0),
                        "current_price": prices[0],
                        "old_price": prices[1] if len(prices) > 1 else 0,
                    }
                )
                results.append(row)

        return results

    async def run(self) -> list[dict]:
        all_products: list[dict] = []

        async with async_playwright() as p:
            api = await p.request.new_context(extra_http_headers=self.HEADERS)
            page_number = 1

            while True:
                data = await self.fetch_page(api, page_number)
                if not data:
                    break

                parsed = self.parse_product(data)
                if not parsed:
                    break

                all_products.extend(parsed)
                logger.info(
                    f"PetShop page {page_number}: +{len(parsed)} items "
                    f"(total={len(all_products)})"
                )

                page_number += 1
                await asyncio.sleep(random.uniform(*self.PAGE_DELAY_RANGE))

            await api.dispose()

        logger.info(f"PetShop parsed total: {len(all_products)} products")
        return all_products
