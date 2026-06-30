from fastapi import Depends

from jose import JWTError, jwt

from app.config.settings import settings

from app.config.security import oauth2_scheme

from repositories.app.user_repository import get_user

from dependencies.database import get_db

from errors.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    UserNotFoundException
)

from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        username = payload.get("sub")

        if not username:
            raise InvalidCredentialsException()

    except JWTError:
        raise InvalidTokenException()

    user = await get_user(
        db,
        username=username
    )

    if not user:
        raise UserNotFoundException(user)

    return user
