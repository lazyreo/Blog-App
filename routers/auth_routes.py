from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database import get_db

from repositories.bot.web_scrape_repository import get_myanimelist

from schemas.user_schemas import (
    UserCreate,
    UserCreateResponse
)

from schemas.auth_schemas import AccessTokenResponse

from services.auth_service import (
    create_user,
    login_user
)

auth_router = APIRouter(
    tags=["Auth"]
)

# Sign - up user


@auth_router.post(
    "/sign-up",
    response_model=UserCreateResponse
)
async def sign_up(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    r = await create_user(
        user,
        db
    )

    return UserCreateResponse(
        status="success",
        user=r
    )

# Login


@auth_router.post(
    "/login",
    response_model=AccessTokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    
    access_token = await login_user(
        form_data,
        db
    )
   
    return AccessTokenResponse(
        access_token=access_token
    )
    
@auth_router.get(
    "/get-links",)
async def get_links():
    return await get_myanimelist()
