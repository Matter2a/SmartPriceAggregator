from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from database.base import Base
from datetime import datetime
class RawProduct(Base):
    __tablename__ = "raw_products"

   
    id: Mapped[int] = mapped_column(primary_key=True)

    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"))
    external_id: Mapped[str] = mapped_column(String(255))

    title: Mapped[str] = mapped_column(String(255))
    raw_weight: Mapped[str] = mapped_column(String(100))
    raw_brand: Mapped[str] = mapped_column(String(255))
    raw_category: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
