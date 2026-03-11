

from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from server.repository.users import UserRepository
from server.repository.products import ProductRepository


def get_user_repository(request: Request) -> UserRepository:
    return UserRepository(request.app.state.db_engine)

def get_product_repository(request: Request) -> ProductRepository:
    return ProductRepository(request.app.state.db_engine)