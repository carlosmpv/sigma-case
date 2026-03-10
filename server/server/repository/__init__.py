

from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncEngine
from server.repository.users import UserRepository

def attach_repositories_to_app(app: FastAPI, engine: AsyncEngine):
    app.state.user_repository = UserRepository(engine)

def get_user_repository(request: Request) -> UserRepository:
    return request.app.state.user_repository