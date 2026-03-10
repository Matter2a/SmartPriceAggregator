from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from database.base import Base
from datetime import datetime

class MasterProduct(Base):
    __tablename__ = "master_product"

    id: Mapped[int] = mapped_column(primary_key=True)

    raw_product_id: Mapped[int] = mapped_column(
        ForeignKey("raw_products.id")
    )

    title_normalized: Mapped[str] = mapped_column(String(255))
    brand_normalized: Mapped[str] = mapped_column(String(255))
    blocking_key: Mapped[str] = mapped_column(String(255))
