from datetime import datetime
from decimal import Decimal
from typing import Optional
import uuid

from pydantic import BaseModel
from .base import Base
from sqlalchemy import ForeignKey, Integer, Numeric, String, func, text, Double
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from geoalchemy2.types import Geometry as GeoType


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

    price_per_quantity: Mapped[Decimal] = mapped_column(
        Numeric(),
        nullable=False
    )

    quantity: Mapped[Decimal] = mapped_column(
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

class ProductTransaction(Base):
    __tablename__ = "products_transaction"

    uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.uuidv7()
    )

    product_uuid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.uuid"),
        nullable=False
    )

    product: Mapped['Product'] = relationship('Product')
    
    quantity: Mapped[Decimal] = mapped_column(
        Numeric(),
        nullable=False
    )

    location: Mapped[GeoType] = mapped_column(
        Geometry('POINT'),
        nullable=False
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
    unit_of_measure: Optional[str] = None

class ProductCreatePayload(BaseModel):
    name: str
    price_per_quantity: float
    unit_of_measure: str

class RegProductTransactionResponse(BaseModel):
    updated_product: ProductResponse
    when: datetime
    quantity: float
    lat: float
    lng: float

    class Config:
        from_attributes = True

class RegProductTransactionPayload(BaseModel):
    quantity: float
    lng: float
    lat: float
    