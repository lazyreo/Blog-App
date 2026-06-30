from fastapi import FastAPI

from contextlib import asynccontextmanager

from db.engine import create_tables

from errors.handlers import register_exception_handlers

from routers.blog_routes import blog_router

from routers.auth_routes import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(blog_router)

app.include_router(auth_router)

register_exception_handlers(app)
