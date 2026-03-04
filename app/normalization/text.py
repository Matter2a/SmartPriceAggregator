import re
from typing import Optional
def clean_text(s: Optional[str]) -> str:
    """Базовая очистка от самого вредного мусора"""
    if not s:
        return ""
    s = str(s).strip()
    
    # 1. Убираем невидимые символы и переносы строк
    s = re.sub(r'[\r\n\t\xa0\u200b\ufeff]', ' ', s)
    
    # 2. Убираем копирайт, декоративные символы
    s = re.sub(r'[©®™•※★☆✪⁕·･║│┃]', '', s)
    
    # 3. Оставляем только полезное: буквы, цифры, пробелы и несколько знаков
    s = re.sub(r'[^a-zA-Z0-9а-яА-ЯёЁ\s\-\+\/×\.,]', '', s)
    
    # 4. Убираем мусор в начале и конце (акции, скидки и т.п.)
    s = re.sub(r'^(акция|новинка|скидка|sale|new|-{2,}|\*+|\s*[!%]{2,}\s*)', '', s, flags=re.I)
    s = re.sub(r'(\s*[!%]{2,}|акция|скидка|sale|\*+|-{2,})$', '', s, flags=re.I)
    
    # 5. Множественные пробелы → один
    s = re.sub(r'\s+', ' ', s)
    
    return s.strip()


def normalize_text(s: str) -> str:
    """Приводим к нижнему регистру + замены типичных букв"""
    if not s:
        return ""
    s = s.lower()
    s = s.replace('ё', 'е')
    return s


def normalize_brand(brand: Optional[str]) -> str:
    if not brand:
        return ""
    brand = clean_text(brand)
    brand = normalize_text(brand)
    
    # Можно добавить словарь замен по мере накопления
    brand_map = {
        'florida vet': 'florida vet',
        'royal canin': 'royalcanin',
        '4 лапы': '4lapy',

    }
    return brand_map.get(brand, brand)


 