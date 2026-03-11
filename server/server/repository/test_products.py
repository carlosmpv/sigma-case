from random import random

import pytest
import pytest_asyncio

from server.database import create_engine
from server.repository.products import ProductRepository
from server.models.base import create_tables
from server.models.product import ProductCreatePayload, ProductUpdatePayload


@pytest_asyncio.fixture()
async def engine():
    engine = create_engine()
    await create_tables(engine)
    yield engine
    await engine.dispose()

@pytest.mark.asyncio
async def test_products_repository(engine):
    product_repository = ProductRepository(engine)
    products = await product_repository.list()
    before_insert_len = len(products)

    test_product_name = f"TestProduct_{before_insert_len}"
    price_per_quantity = random() * 100
    quantity = random() * 1000
    unit_of_measure = 'km'

    new_product = await product_repository.create(
        payload=ProductCreatePayload(
            name=test_product_name,
            price_per_quantity=price_per_quantity,
            quantity=quantity,
            unit_of_measure=unit_of_measure,
        )
    )

    products = await product_repository.list()
    assert len(products) == before_insert_len + 1
    
    recovered_product = await product_repository.by_id(new_product.uuid)
    assert recovered_product is not None
    assert recovered_product.name == test_product_name
    assert recovered_product.price_per_quantity == price_per_quantity
    assert recovered_product.quantity == quantity
    assert recovered_product.unit_of_measure == unit_of_measure

    new_price_per_quantity = random() * 100
    new_quantity = random() * 1000
    new_unit_of_measure = 'L'
    await product_repository.update_by_id(
        new_product.uuid, 
        update_payload=ProductUpdatePayload(
            price_per_quantity=new_price_per_quantity,
            quantity=new_quantity,
            unit_of_measure=new_unit_of_measure
        )
    )

    recovered_product = await product_repository.by_id(new_product.uuid)
    assert recovered_product is not None
    assert recovered_product.price_per_quantity == new_price_per_quantity
    assert recovered_product.quantity == new_quantity
    assert recovered_product.unit_of_measure == new_unit_of_measure

    await product_repository.delete_by_id(new_product.uuid)
    products = await product_repository.list()
    assert len(products) == before_insert_len