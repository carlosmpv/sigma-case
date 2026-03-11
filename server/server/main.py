

from contextlib import asynccontextmanager

from fastapi import FastAPI

from server.database import create_engine
from server.endpoints import authentication_router
from server.endpoints.secured import secured_router
from server.models.base import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_engine = create_engine()
    await create_tables(app.state.db_engine)

    yield

    await app.state.db_engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(authentication_router)
app.include_router(secured_router)