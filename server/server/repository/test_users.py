

from random import randint
import secrets

import pytest
import pytest_asyncio

from server.database import create_engine
from server.models.base import create_tables
from server.repository.users import CreateUserPayload, UserRepository
from server.models.users import User


@pytest_asyncio.fixture()
async def engine():
    engine = create_engine()
    await create_tables(engine)
    yield engine
    await engine.dispose()

@pytest.mark.asyncio
async def test_users_repository(engine):
    user_repository = UserRepository(engine)
    
    username = f"TestUser_{randint(0, 10000)}"
    password = secrets.token_urlsafe(16)
    payload = CreateUserPayload(
        username=username,
        password=password,
    )

    await user_repository.create_user(payload)
    
    user = await user_repository.find_by_username_and_password(username, password)
    assert user is not None
    assert user.username == username

    recovered_user = await user_repository.find_by_userid(user.uuid)
    assert recovered_user is not None
    assert recovered_user.username == username
