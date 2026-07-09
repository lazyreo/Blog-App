
from fastapi import FastAPI

from contextlib import asynccontextmanager

from loguru import logger

from db.engine import create_tables

from errors.handlers import register_exception_handlers

from routers.blog_routes import blog_router

from routers.auth_routes import auth_router

from db.session import AsyncSessionLocal

from db.engine import seed_bots


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()

    async with AsyncSessionLocal() as db:

        logger.info("Seeding bots...")
        await seed_bots(db)
        logger.info("Successfully created bots!")

    yield

try:
    app = FastAPI(lifespan=lifespan)

    app.include_router(blog_router)
    app.include_router(auth_router)

    register_exception_handlers(app)
except Exception as e:
    logger.critical(f"Unable to configue settings: {e}")
