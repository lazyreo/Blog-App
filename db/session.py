from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession
)

from db.engine import engine

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=True,
    expire_on_commit=False
)
