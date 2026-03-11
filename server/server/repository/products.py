from typing import List, Optional
import uuid

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from server.exceptions import unknown_product_exception
from server.models.product import Product, ProductCreatePayload, ProductUpdatePayload, ProductResponse
from server.exceptions import product_already_created_exception

class ProductRepository:
    def __init__(self, engine: AsyncEngine) -> None:
        self.async_session = async_sessionmaker(engine, expire_on_commit=False)

    async def list(self) -> List[ProductResponse]:
        stmt = select(Product)

        async with self.async_session() as session:
            result = await session.scalars(stmt)
            return [ProductResponse.model_validate(res) for res in result]
        
    async def by_id(self, id: uuid.UUID) -> Optional[ProductResponse]:
        stmt = (
            select(Product)
            .where(Product.uuid == id)
        )

        async with self.async_session() as session:
            result = await session.scalar(stmt)
            return ProductResponse.model_validate(result)

        
    async def create(self, payload: ProductCreatePayload) -> ProductResponse:
        new_product = Product(**payload.model_dump()) # é tudo chave valor (sempre foi)

        try:
            async with self.async_session() as session:
                async with session.begin():
                    session.add(new_product)

                return ProductResponse.model_validate(new_product)
            
        except IntegrityError:
            raise product_already_created_exception


    async def update_by_id(self, id: uuid.UUID, update_payload: ProductUpdatePayload):
        select_stmt = (
            select(Product)
            .where(Product.uuid == id)
        )

        async with self.async_session() as session:
            async with session.begin():
                target = await session.scalar(select_stmt)
            
                if target is None:
                    raise unknown_product_exception
                
                for k, v in update_payload.model_dump().items():
                    if v is not None:
                        setattr(target, k , v)


    async def delete_by_id(self, id: uuid.UUID):
        delete_stmt = (
            delete(Product)
            .where(Product.uuid == id)
        )

        async with self.async_session() as session:
            async with session.begin():
                await session.execute(delete_stmt)

                
    