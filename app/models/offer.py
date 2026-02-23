from sqlalchemy import String, DateTime, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from database.base import Base
from datetime import datetime
class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(primary_key=True)
    master_product_id: Mapped[int] = mapped_column(
        ForeignKey("master_product.id")
    )

    raw_product_id: Mapped[int] = mapped_column(
        ForeignKey("raw_products.id")
    )

    shop_id: Mapped[int] = mapped_column(
        ForeignKey("shops.id")
    )

    current_price: Mapped[float] = mapped_column(Float)
    old_price: Mapped[float] = mapped_column(Float, nullable=True)
    discount: Mapped[int] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now( ))