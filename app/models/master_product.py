from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from database.base import Base
from datetime import datetime
class MasterProduct(Base):
    __tablename__ = "master_product"

    id: Mapped[int] = mapped_column(primary_key=True)
    normalized_name: Mapped[str] = mapped_column(String(255), nullable=False)
    brand: Mapped[str] = mapped_column(String(255), nullable=False)
    weight_grams: Mapped[int] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())