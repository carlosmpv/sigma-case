
from typing import Annotated

from fastapi import APIRouter, Depends

from server.repository import MapRepository, get_map_repository

router = APIRouter()

MapRepositoryDependency = Annotated[MapRepository, Depends(get_map_repository)]

@router.get("/map/features")
async def get_map_features(
    map_repository: MapRepositoryDependency
):
    """
    Obtem os GeoJSON que devem ser apresentados no mapa
    """
    return await map_repository.get_all_features()


@router.get("/map/soil_usage")
async def get_soil_usage(
    map_repository: MapRepositoryDependency
):
    """
    Obtem a lista de usos de solo juntamente com suas areas
    """
    return await map_repository.get_soil_usage()