from sqlalchemy.ext.asyncio import create_async_engine

from app.config.settings import settings

from models import (
    base,
    blog_model,
    user_model

)

engine = create_async_engine(
    settings.POSTGRESQL_URL
)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(base.Base.metadata.create_all)
