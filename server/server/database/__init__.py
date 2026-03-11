

import os
from sqlalchemy.ext.asyncio import create_async_engine

__postgres_password = os.getenv('POSTGRES_PASSWORD')
__postgres_password_file = os.getenv('POSTGRES_PASSWORD_FILE')
if __postgres_password_file is None and __postgres_password is None:
    raise RuntimeError("Either POSTGRES_PASSWORD or POSTGRES_PASSWORD_FILE must be defined")

__postgres_user = os.getenv('POSTGRES_USER')
if __postgres_user is None:
    raise RuntimeError('POSTGRES_USER must be defined')

__postgres_db = os.getenv('POSTGRES_DB')
if __postgres_db is None:
    raise RuntimeError('POSTGRES_DB must be defined')

__postgres_host = os.getenv('POSTGRES_HOST')
if __postgres_host is None:
    raise RuntimeError('POSTGRES_HOST must be defined')

if __postgres_password_file is not None:
    with open(__postgres_password_file, 'r') as postgres_password_file:
        __postgres_password = postgres_password_file.read()

def create_engine():
    return create_async_engine(
        url = f"postgresql+asyncpg://{__postgres_user}:{__postgres_password}@{__postgres_host}:5432/{__postgres_db}",
        echo = True
    )
