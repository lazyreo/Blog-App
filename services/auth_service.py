
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordRequestForm

from jose import jwt
from loguru import logger

from app.config import security

from app.config.settings import settings

from repositories.app import user_repository

from errors.exceptions import InvalidCredentialsException, UsernameAlreadyTakenException

from schemas import user_schemas

from sqlalchemy.ext.asyncio import AsyncSession

from models.user_model import User

from sqlalchemy.exc import IntegrityError


# Create user


async def create_user(
    user: user_schemas.UserCreate,
    db: AsyncSession
) -> user_schemas.UserCreateResponse:
    is_exists = await user_repository.check_user(
        db=db,
        username=user.username,
        email=user.email
    )

    if is_exists:
        raise UsernameAlreadyTakenException(user.username)

    hashed_password = security.hash_password(
        user.password
    )

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )

    try:
        db.add(db_user)
        await db.commit()

    except IntegrityError:
        await db.rollback()
        logger.exception("DB rollback")
        raise UsernameAlreadyTakenException(user.username)

    await db.refresh(db_user)

    return db_user

# Authenticate user


async def authenticate_user(
    username: str,
    password: str,
    db: AsyncSession
) -> User | None:
    user: User = await user_repository.get_user(
        db,
        username=username
    )

    if not user:
        return None

    if not security.verify_password(
        password,
        user.password_hash
    ):
        return None

    return user


# Create token


async def create_access_token(
    data: dict,
    expire_dur: timedelta | None = None
) -> str:
    to_encode = data.copy()

    if expire_dur is None:
        expire_dur = datetime.now(tz=timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update(
        {
            "exp": expire_dur
        }
    )

    return jwt.encode(
        claims=to_encode,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

# Login


async def login_user(
    form_data: OAuth2PasswordRequestForm,
    db: AsyncSession
):
    is_authenticated = await authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=db
    )

    if not is_authenticated:
        raise InvalidCredentialsException

    user: User = is_authenticated

    data = {
        "sub": user.username
    }

    access_token = await create_access_token(
        data
    )

    return access_token
