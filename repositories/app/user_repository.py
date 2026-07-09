from sqlalchemy import Result, exists, select

from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import EmailStr

from models import user_model

from loguru import logger

# Read a user


async def get_user(
    db: AsyncSession,
    user_id: int | None = None,
    username: str | None = None,
    email: EmailStr | None = None,
) -> user_model.User | None:

    if user_id is not None:
        result = await db.execute(
            select(
                user_model.User
            ).where(
                user_model.User.id == user_id
            )
        )

    elif username is not None:
        result = await db.execute(
            select(
                user_model.User
            ).where(
                user_model.User.username == username
            )
        )

    elif email is not None:
        result = await db.execute(
            select(
                user_model.User
            ).where(
                user_model.User.email == email
            )
        )

    else:
        return None

    user = result.scalar_one_or_none()

    return user


# Check a user


async def check_user(

    db: AsyncSession,
    user_id: int | None = None,
    username: str | None = None,
    email: EmailStr | None = None,

) -> bool | None:

    if user_id is not None:
        condition = user_model.User.id == user_id
    elif username is not None:
        condition = user_model.User.username == username
    elif email is not None:
        condition = user_model.User.email == email
    else:
        return None

    result: Result = await db.execute(
        select(
            exists().where(
                condition
            )
        )
    )

    return bool(result.scalar_one_or_none())
