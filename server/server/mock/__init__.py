import json
from pathlib import Path
import aiofiles
from sqlalchemy.ext.asyncio import AsyncEngine

from server.repository.map import MapRepository

server_module_path = Path(__file__).parent.parent
assets_path = server_module_path / "assets"
geojson_feature_collection_file = assets_path / "uso_ocupacao_teste.geojson"

async def populate_map(db_engine: AsyncEngine):
    map_repository = MapRepository(db_engine)
    is_populated = await map_repository.is_populated()
    if not is_populated:
        async with aiofiles.open(geojson_feature_collection_file) as file:
            content = await file.read()
            feature_collection = json.loads(content)

        await map_repository.import_feature_collection(feature_collection)