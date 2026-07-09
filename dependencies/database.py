
from functools import wraps

from db.session import AsyncSessionLocal

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db


def with_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            try:
                result = await func(*args, db=db, **kwargs)
                await db.commit()
                return result
            except Exception:
                await db.rollback()
                raise

    return wrapper
