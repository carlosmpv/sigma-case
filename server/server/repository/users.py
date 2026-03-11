

from typing import Optional
import uuid

from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlalchemy import Engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from server.models.users import User
from server.exceptions import username_already_in_use

password_hash = PasswordHash.recommended()

class UserRepository:
    def __init__(self, engine: AsyncEngine):
        self.async_session = async_sessionmaker(engine, expire_on_commit=False)
        

    async def find_by_username_and_password(self, username: str, password: str) -> Optional[User]:
        stmt = (
            select(User)
            .where(User.username == username)
        )

        async with self.async_session() as session:
            user = await session.scalar(stmt)

        if user is None:
            return None
        
        if not password_hash.verify(password, user.passhash):
            return None
        
        return user
        
    async def find_by_userid(self, userid: uuid.UUID):
        stmt = (
            select(User)
            .where(User.uuid == userid)
        )

        async with self.async_session() as session:
            return await session.scalar(stmt)
        
    async def create_user(self, payload: CreateUserPayload):
        new_user = User(
            username=payload.username,
            passhash=password_hash.hash(payload.password),
        )

        try:    
            async with self.async_session() as session:
                async with session.begin():
                    session.add(new_user)

        except IntegrityError:
            raise username_already_in_use

class CreateUserPayload(BaseModel):
    username: str
    password: str