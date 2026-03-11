import pytest

from server.database import create_engine
from server.repository.products import ProductRepository
from server.models.base import create_tables


# @pytest.fixture()
# async def engine():
    
#     yield engine
#     await engine.dispose()

@pytest.mark.asyncio
async def test_products_repository():
    engine = create_engine()
    await create_tables(engine)

    product_repository = ProductRepository(engine)
    
    products = await product_repository.list()
    await engine.dispose()