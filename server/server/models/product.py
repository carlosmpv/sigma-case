from typing import Optional
import uuid

from pydantic import BaseModel
from .base import Base
from sqlalchemy import Integer, Numeric, String, func, text, Double
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

class Product(Base):
    __tablename__ = "products"

    uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.uuidv7()
    )

    name: Mapped[str] = mapped_column(
        String(),
        unique=True,
        nullable=False,
    )

    price_per_quantity: Mapped[float] = mapped_column(
        Numeric(),
        nullable=False
    )

    quantity: Mapped[float] = mapped_column(
        Numeric(),
        default=0,
        server_default=text("0"),
        nullable=False
    )

    unit_of_measure: Mapped[str] = mapped_column(
        String(),
        default='un',
        server_default=text("'un'"),
        nullable=False,
    )

class ProductResponse(BaseModel):
    uuid: uuid.UUID
    name: str
    price_per_quantity: float
    quantity: float
    unit_of_measure: str

    class Config:
        from_attributes = True

class ProductUpdatePayload(BaseModel):
    name: Optional[str] = None
    price_per_quantity: Optional[float] = None
    quantity: Optional[float] = None
    unit_of_measure: Optional[str] = None

class ProductCreatePayload(BaseModel):
    name: str
    price_per_quantity: float
    quantity: float
    unit_of_measure: str