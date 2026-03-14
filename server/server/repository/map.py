import json
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from sqlalchemy import select, func
from geoalchemy2.functions import ST_GeomFromGeoJSON, ST_AsGeoJSON, ST_Area, ST_Transform

from server.models.map import Feature, FeatureCollection, GeoFeature, SoilUsage
import re

def _rgb_to_hex(rgbstr: str) -> str:
    result = re.findall(r'rgb\(\s*(\d+),\s*(\d+),\s*(\d+)\)', rgbstr)
    if len(result) != 1:
        return '#000000'
    
    (r, g, b) = (int(r) for r in result[0])
    return '#%02x%02x%02x' % (r, g, b)

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
                        k: (
                            _rgb_to_hex(v) if k == 'rgb'
                            else v
                        )
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
        stmt = select(
            GeoFeature,
            ST_AsGeoJSON(GeoFeature.geometry).label("geometry_geojson")
        )
        async with self.async_session() as session:
            
            features = []
            for feature, geometry_geojson in await session.execute(stmt):
                polygon = json.loads(geometry_geojson)

                properties = {
                    col.name: getattr(feature, col.name)
                    for col in GeoFeature.__table__.columns
                    if col.name != 'geometry'
                }

                features.append(
                    Feature(
                        properties=properties,
                        geometry=polygon
                    )
                )

            return FeatureCollection(features=features)
        
    async def get_soil_usage(self) -> List[SoilUsage]:
        # A area nesta solução não batem com o que está registrado
        # mas seria uma forma de se obter a area da geometria
        # 
        # stmt = select(
        #     GeoFeature.desc_uso_solo,
        #     GeoFeature.rgb,
        #     func.sum(ST_Area(ST_Transform(GeoFeature.geometry, 5880)))
        # ).group_by(GeoFeature.desc_uso_solo, GeoFeature.rgb)

        stmt = select(
            GeoFeature.desc_uso_solo,
            GeoFeature.rgb,
            GeoFeature.area_ha
        )

        async with self.async_session() as session:
            return [
                SoilUsage(
                    desc_uso_solo=desc,
                    rgb=rgb,
                    area=area,
                )
                
                for desc, rgb, area in await session.execute(stmt)
            ]
