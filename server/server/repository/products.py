from decimal import Decimal
from typing import List, Optional
import uuid

from sqlalchemy import delete, func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from server.exceptions import unknown_product_exception
from server.models.product import Product, ProductCreatePayload, ProductTransaction, ProductUpdatePayload, ProductResponse, RegProductTransactionResponse
from server.exceptions import product_already_created_exception
from geoalchemy2.functions import ST_MakePoint, ST_X, ST_Y

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

                
    async def reg_buy_product(self, productID: uuid.UUID, quantity: float, lng: float, lat: float) -> RegProductTransactionResponse:
        async with self.async_session() as session:
            async with session.begin():
                target_product = await session.get(Product, productID)
                if target_product is None:
                    raise unknown_product_exception
                
                reg_transaction = ProductTransaction(
                    product=target_product,
                    quantity=quantity,
                    location=ST_MakePoint(lng, lat)
                )

                target_product.quantity += Decimal(str(quantity))
                session.add(reg_transaction)

                await session.flush()
                return RegProductTransactionResponse(
                    updated_product=ProductResponse.model_validate(target_product),
                    when=reg_transaction.created_at,
                    quantity=quantity,
                    lat=lat,
                    lng=lng
                )
            
    async def reg_sell_product(self, productID: uuid.UUID, quantity: float, lng: float, lat: float) -> RegProductTransactionResponse:
        async with self.async_session() as session:
            async with session.begin():
                target_product = await session.get(Product, productID)
                if target_product is None:
                    raise unknown_product_exception
                
                if target_product.quantity is None:
                    raise 
                
                reg_transaction = ProductTransaction(
                    product=target_product,
                    quantity=quantity,
                    location=ST_MakePoint(lng, lat)
                )

                target_product.quantity -= Decimal(str(quantity))
                session.add(reg_transaction)

                await session.flush()
                return RegProductTransactionResponse(
                    updated_product=ProductResponse.model_validate(target_product),
                    when=reg_transaction.created_at,
                    quantity=-quantity,
                    lat=lat,
                    lng=lng
                )
            
    async def current_cash(self):
        query = select(
            func.sum(ProductTransaction.quantity * Product.price_per_quantity)
        ).join(
            ProductTransaction.product
        )
        
        async with self.async_session() as session:
            result = await session.scalar(query)
            return result
        
    async def transaction_history(self):
        stmt = select(
            ProductTransaction,
            ST_X(ProductTransaction.location).label('lng'),
            ST_Y(ProductTransaction.location).label('lat'),
        ).options(
            selectinload(ProductTransaction.product)  # Carrega o produto junto
        )
        async with self.async_session() as session:
            result = await session.execute(stmt)
            return [
                RegProductTransactionResponse(
                    lng=lng,
                    lat=lat,
                    updated_product=transaction.product,
                    when=transaction.created_at,
                    quantity=transaction.quantity,
                )

                for transaction, lng, lat in result.all()
            ]