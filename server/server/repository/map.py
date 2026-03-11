import json
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from sqlalchemy import select, func
from geoalchemy2.functions import ST_GeomFromGeoJSON, ST_AsGeoJSON

from server.models.geo_feature import GeoFeature

class MapRepository:
    def __init__(self, engine: AsyncEngine) -> None:
        self.async_session = async_sessionmaker(engine, expire_on_commit=False)

    async def import_feature_collection(self, feature_collection: dict):
        table_columns = [
            key for key in 
            GeoFeature.__table__.columns.keys()
            if key != "uuid"
        ]

        async with self.async_session() as session:
            async with session.begin():
                features: List[Dict[str, Any]] = feature_collection.get("features", [])
                for feature in features:
                    properties: Dict[str, Any] = feature.pop("properties", {})
                    flattened = {**feature, **properties}
                    filtered = {
                        k: v
                        for k, v in flattened.items()
                        if k in table_columns
                    }

                    filtered['geometry'] = ST_GeomFromGeoJSON(json.dumps(feature.get('geometry')))
                    geo_feature = GeoFeature(**filtered)
                    session.add(geo_feature)

    async def is_populated(self):
        stmt = select(func.count()).select_from(GeoFeature)
        async with self.async_session() as session:
            feature_count = await session.scalar(stmt)
            return (feature_count is not None and feature_count > 0)
        
    async def get_all_features(self):
        stmt = select(ST_AsGeoJSON(GeoFeature.geometry)).select_from(GeoFeature)
        async with self.async_session() as session:
            features = await session.scalars(stmt)
            return list(features)