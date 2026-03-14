from typing import Any, Dict, List
import uuid
from pydantic import BaseModel
from sqlalchemy import UUID, Float, String, func

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geometry
from geoalchemy2.types import Geometry as GeoType

class GeoFeature(Base):
    __tablename__ = "geo_feature"

    uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.uuidv7()
    )

    desc_uso_solo: Mapped[str] = mapped_column(
        String(),
        nullable=False
    )

    rgb: Mapped[str] = mapped_column(
        String(),
        default='#000000'
    )

    area_ha: Mapped[float] = mapped_column(
        Float(),
        default=0
    )

    geometry: Mapped[GeoType] = mapped_column(
        Geometry("MULTIPOLYGON")
    )

class Feature(BaseModel):
    type: str = "Feature"
    id: uuid.UUID
    properties: Dict[str, Any] = {}
    geometry: Any

class FeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[Feature]

class SoilUsage(BaseModel):
    id: uuid.UUID
    desc_uso_solo: str
    rgb: str
    area: float