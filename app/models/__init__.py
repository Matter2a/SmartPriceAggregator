# models/__init__.py

from database.base import Base

# Импортируем ВСЕ модели — это заставит их зарегистрироваться в Base.metadata
from .shop import Shop
from .raw_product import RawProduct
from .master_product import MasterProduct
from .offer import Offer

# если будут новые модели — добавляй сюда же