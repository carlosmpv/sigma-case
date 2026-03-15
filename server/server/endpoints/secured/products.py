

from typing import Annotated, List, Optional
import uuid

from fastapi import Depends
from fastapi.routing import APIRouter

from server.models.product import ProductCreatePayload, ProductUpdatePayload, ProductResponse, RegProductTransactionPayload
from server.repository import get_product_repository
from server.repository.products import ProductRepository

router = APIRouter()

ProductRepositoryDependency = Annotated[ProductRepository, Depends(get_product_repository)]

@router.post("/products")
async def create_product(
    product_repository: ProductRepositoryDependency,
    product_create_payload: ProductCreatePayload
):
    return await product_repository.create(product_create_payload)
    

@router.get("/products")
async def list_products(
    product_repository: ProductRepositoryDependency
) -> List[ProductResponse]:
    return await product_repository.list()

@router.get("/products/{product_id}")
async def get_product(
    product_repository: ProductRepositoryDependency,
    product_id: str,
) -> Optional[ProductResponse]:
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

@router.get("/transaction/history")
async def transaction_history(
    product_repository: ProductRepositoryDependency,
):
    return await product_repository.transaction_history()

@router.post("/transaction/buy/{product_id}")
async def reg_buy_product(
    product_repository: ProductRepositoryDependency,
    product_id: str,
    transaction_info: RegProductTransactionPayload,
):
    return await product_repository.reg_buy_product(
        productID=uuid.UUID(product_id),
        **transaction_info.model_dump()
    )

@router.post("/transaction/sell/{product_id}")
async def reg_sell_product(
    product_repository: ProductRepositoryDependency,
    product_id: str,
    transaction_info: RegProductTransactionPayload,
):
    return await product_repository.reg_sell_product(
        productID=uuid.UUID(product_id),
        **transaction_info.model_dump()
    )

@router.get("/transaction/total")
async def transaction_total(
    product_repository: ProductRepositoryDependency,
):
    return await product_repository.current_cash()