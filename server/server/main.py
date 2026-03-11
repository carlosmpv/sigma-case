

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from server.database import create_engine
from server.endpoints import authentication_router
from server.endpoints.secured import secured_router
from server.models.base import create_tables
from server.mock import populate_map

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_engine = create_engine()
    await create_tables(app.state.db_engine)
    await populate_map(app.state.db_engine)

    yield

    await app.state.db_engine.dispose()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    GZipMiddleware,
    minimum_size=1024,
    compresslevel=6,
)

app.include_router(authentication_router)
app.include_router(secured_router)