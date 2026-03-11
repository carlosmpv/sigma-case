

from typing import Annotated, List, Optional
import uuid

from fastapi import Depends
from fastapi.routing import APIRouter

from server.models.product import Product, ProductCreatePayload, ProductUpdatePayload
from server.repository import get_product_repository
from server.repository.products import ProductRepository

router = APIRouter()

ProductRepositoryDependency = Annotated[ProductRepository, Depends(get_product_repository)]

@router.post("/products")
async def create_product(
    product_repository: ProductRepositoryDependency,
    product_create_payload: ProductCreatePayload
):
    await product_repository.create(product_create_payload)

@router.get("/products")
async def list_products(
    product_repository: ProductRepositoryDependency
) -> List[Product]:
    return await product_repository.list()

@router.get("/products/{product_id}")
async def get_product(
    product_repository: ProductRepositoryDependency,
    product_id: str,
) -> Optional[Product]:
    return await product_repository.by_id(uuid.UUID(product_id))

@router.put("/products/{product_id}")
async def update_product(
    product_repository: ProductRepositoryDependency,
    product_id: str,
    changes: ProductUpdatePayload
):
    await product_repository.update_by_id(uuid.UUID(product_id), changes)

@router.delete("/products/{product_id}")
async def delete_product(
    product_repository: ProductRepositoryDependency,
    product_id: str,
):
    await product_repository.delete_by_id(uuid.UUID(product_id))