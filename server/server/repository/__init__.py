

from fastapi import Request
from server.repository.users import UserRepository
from server.repository.products import ProductRepository
from server.repository.map import MapRepository


def get_user_repository(request: Request) -> UserRepository:
    return UserRepository(request.app.state.db_engine)

def get_product_repository(request: Request) -> ProductRepository:
    return ProductRepository(request.app.state.db_engine)

def get_map_repository(request: Request) -> MapRepository:
    return MapRepository(request.app.state.db_engine)