from sqlalchemy.ext.asyncio import create_async_engine

from app.config.security import hash_password

from models import (
    base,
    blog_model,  # noqa: F401
    user_model  # noqa: F401
)

from sqlalchemy import select

from app.config.settings import settings

from sqlalchemy.ext.asyncio import AsyncSession

BOT_USERS = [
    {
        "username": "Bot1",
        "email": None,
        "password_hash": hash_password(settings.BOT1_PASSWORD),
    },
    {
        "username": "Bot2",
        "email": None,
        "password_hash": hash_password(settings.BOT2_PASSWORD),
    },
    {
        "username": "Bot3",
        "email": None,
        "password_hash": hash_password(settings.BOT3_PASSWORD),
    },
]


async def seed_bots(db: AsyncSession):
    for bot in BOT_USERS:
        exists = await db.scalar(
            select(user_model.User).where(
                user_model.User.username == bot["username"]
            )
        )

        if exists is None:
            db.add(user_model.User(**bot))

    await db.commit()

engine = create_async_engine(
    settings.POSTGRESQL_URL
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(base.Base.metadata.create_all)
    