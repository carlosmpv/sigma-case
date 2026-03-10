

import os
from sqlalchemy.ext.asyncio import create_async_engine

__postgres_password_file = os.getenv('POSTGRES_PASSWORD_FILE')
if __postgres_password_file is None:
    raise RuntimeError("POSTGRES_PASSWORD_FILE must be defined")

__postgres_user = os.getenv('POSTGRES_USER')
if __postgres_user is None:
    raise RuntimeError('POSTGRES_USER must be defined')

__postgres_db = os.getenv('POSTGRES_DB')
if __postgres_db is None:
    raise RuntimeError('POSTGRES_DB must be defined')

__postgres_host = os.getenv('POSTGRES_HOST')
if __postgres_host is None:
    raise RuntimeError('POSTGRES_HOST must be defined')

with open(__postgres_password_file, 'r') as postgres_password_file:
    postgres_password = postgres_password_file.read()

def create_engine():
    return create_async_engine(url = f"postgresql+asyncpg://{__postgres_user}:{postgres_password}@{__postgres_host}/{__postgres_db}")
