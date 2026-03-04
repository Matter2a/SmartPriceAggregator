from normalization.text import clean_text, normalize_text, normalize_brand
from typing import Optional
import re
class ProductNormalizer():
    def simple_normalize(raw_title: Optional[str], raw_brand: Optional[str]) -> str:
        """Пример полной цепочки для теста"""
        title_clean = clean_text(raw_title)
        brand_norm = normalize_brand(raw_brand)
    
        # Убираем бренд из названия, если он там есть
        title_no_brand = re.sub(re.escape(brand_norm), '', title_clean, flags=re.I).strip()
    
        # приводим к нижнему регистру
        result = normalize_text(title_no_brand or title_clean)
    
        return result

#Допилить нормализацию веса улучшить код очистки сделать blocking_key