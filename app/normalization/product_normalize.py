from normalization.text import clean_text, normalize_text, normalize_brand
from normalization.weight import remove_weight_from_title
from normalization.blocking_key import make_blocking_key
from typing import Optional
import re
class ProductNormalizer():
    @staticmethod
    def normalize_product(raw_title: Optional[str], raw_brand: Optional[str], weight_grams: Optional[int]) -> dict:
        title = clean_text(raw_title)
        
        # Удаляем вес
        title = remove_weight_from_title(title)
        brand = normalize_brand(raw_brand)

        # Убираем бренд из названия, если он там есть
        title = re.sub(re.escape(brand), '', title, flags=re.I).strip()

        title = normalize_text(title)
        
        blocking_key = make_blocking_key(
            norm_brand=brand,
            norm_title=title,
            weight_grams=weight_grams,
        )
    
        return {
            "title_normalized": title,
            "brand_normalized": brand,
            "blocking_key": blocking_key,
        }

#Допилить нормализацию веса улучшить код очистки сделать blocking_key