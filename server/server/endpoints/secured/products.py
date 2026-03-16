

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
    """
    Registra um novo produto
    """
    return await product_repository.create(product_create_payload)
    

@router.get("/products")
async def list_products(
    product_repository: ProductRepositoryDependency
) -> List[ProductResponse]:
    """
    Lista produtos registrados
    """
    return await product_repository.list()

@router.get("/products/{product_id}")
async def get_product(
    product_repository: ProductRepositoryDependency,
    product_id: str,
) -> Optional[ProductResponse]:
    """
    Obtem um produto por ID
    """
    return await product_repository.by_id(uuid.UUID(product_id))

@router.put("/products/{product_id}")
async def update_product(
    product_repository: ProductRepositoryDependency,
    product_id: str,
    changes: ProductUpdatePayload
):
    """
    Atualiza informações de um produto
    """
    await product_repository.update_by_id(uuid.UUID(product_id), changes)

@router.delete("/products/{product_id}")
async def delete_product(
    product_repository: ProductRepositoryDependency,
    product_id: str,
):
    """
    Exclui um produto
    """
    await product_repository.delete_by_id(uuid.UUID(product_id))

@router.get("/transaction/history")
async def transaction_history(
    product_repository: ProductRepositoryDependency,
):
    """
    Obtem o histórico de compras e vendas dos produtos
    """
    return await product_repository.transaction_history()

@router.post("/transaction/buy/{product_id}")
async def reg_buy_product(
    product_repository: ProductRepositoryDependency,
    product_id: str,
    transaction_info: RegProductTransactionPayload,
):
    """
    Registra a compra de um produto

    **requer que o produto esteja cadastrado**
    """
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
    """
    Registra a venda de um produto

    **requer que o produto esteja cadastrado**
    """
    return await product_repository.reg_sell_product(
        productID=uuid.UUID(product_id),
        **transaction_info.model_dump()
    )

@router.get("/transaction/total")
async def transaction_total(
    product_repository: ProductRepositoryDependency,
):
    """
    Obtem o caixa total a partir das transações realizadas
    """
    return await product_repository.current_cash()