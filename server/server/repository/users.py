

from typing import Optional
import uuid

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from server.models.users import User

class UserRepository:
    def __init__(self, engine: AsyncEngine):
        self.async_session = async_sessionmaker(engine)
        

    async def find_by_username(self, username: str) -> Optional[User]:
        stmt = (
            select(User)
            .where(User.username == username)
        )

        async with self.async_session() as session:
            return await session.scalar(stmt)
        
    async def find_by_userid(self, userid: uuid.UUID):
        stmt = (
            select(User)
            .where(User.uuid == userid)
        )

        async with self.async_session() as session:
            return await session.scalar(stmt)
        
    async def create_user(self, new_user: User):
        async with self.async_session() as session:
            async with session.begin():
                session.add(new_user)
