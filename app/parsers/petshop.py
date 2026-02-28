import time
import random
import json
from playwright.async_api import async_playwright
import asyncio



class PetShopParser:

    BASE_API = "https://www.petshop.ru/api/v4/site/catalog/products/"

    PARAMS = {
        "cityId": 21,
        "categoryId": 926,
        "orderingId": 1
    }

    RETRIES = 3

    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.petshop.ru/"
    }

    async def fetch_page(self, page, page_number):
        params = self.PARAMS.copy()
        params["page"] = page_number

        retry_statuses = {429, 500, 502, 503, 504}

        for attempt in range(self.RETRIES):
            response = await page.request.get(
                self.BASE_API,
                params=params,
                headers=self.HEADERS
            )

            if response.status == 200:
                return await response.json()

            if response.status in retry_statuses:
                await asyncio.sleep(1 + attempt)
                continue

            if response.status == 400:
                return None

        return None

    def parse_product(self, data):
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
                row.update({
                    "variant_id": variant.get("id"),
                    "weight_g": variant.get("weight", 0),
                    "current_price": prices[0],
                    " ": prices[1] if len(prices) > 1 else 0,
                })

                results.append(row)

        return results

    async def run(self):
        all_products = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            await page.goto(
                "https://www.petshop.ru/catalog/cats/food/",
                wait_until="domcontentloaded"
            )

            page_number = 1

            while True:
                data = await self.fetch_page(page, page_number)

                if not data:
                    break

                parsed = self.parse_product(data)

                if not parsed:
                    break

                all_products.extend(parsed)

                print(
                    f"Page {page_number} -> {len(parsed)} items "
                    f"(total: {len(all_products)})"
                )

                page_number += 1
                await asyncio.sleep(0.8 + random.uniform(0, 0.6))

            await browser.close()
            print(f"Перед сохранением: {len(all_products)} продуктов")
            print("Первые 2 элемента:", all_products[:2] if data else "пусто")
        return all_products