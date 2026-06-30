

from fastapi import Depends, APIRouter

from dependencies.auth import get_current_user

from models.user_model import User

from schemas import blog_schemas

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database import get_db

from services import blog_service


blog_router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)


# Post a blog


@blog_router.post(
    "/",
    response_model=blog_schemas.BlogEditResponse)
async def post_blog(
    blog: blog_schemas.BlogPost,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    posted_blog = await blog_service.post_blog(
        blog=blog,
        user=user,
        db=db
    )

    return blog_schemas.BlogEditResponse(
        status="success",
        message="Blog created successfully",
        blog=posted_blog,  # type: ignore
    )


# Get all blogs


@blog_router.get(
    "/",
    response_model=list[blog_schemas.BlogResponse]
)
async def get_blogs(
    page: int = 1,
    limit: int = 10,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    return await blog_service.get_blogs(
        db,
        page,
        limit
    )

# Get blog with ID


@blog_router.get(
    "/{id}",
    response_model=blog_schemas.BlogResponse
)
async def get_blog_by_id(
    blog_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    blog = await blog_service.get_blog(
        blog_id,
        db
    )

    return blog  # type: ignore


# Get blogs of user


@blog_router.get(
    "/",
    response_model=list[blog_schemas.BlogResponse]
)
async def get_blogs_of_user(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    return await blog_service.get_blogs_of_user(
        user,
        db
    )


# Update blog


@blog_router.put(
    "/{id}",
    response_model=blog_schemas.BlogEditResponse
)
async def update_blog(
    blog_id: int,
    updated_blog: blog_schemas.BlogUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    updated_blog = await blog_service.update_blog(
        blog_id,
        updated_blog,
        user,
        db
    )

    return blog_schemas.BlogEditResponse(
        status="success",
        message=f"Blog with ID {blog_id} updated successfully",
        blog=updated_blog,
    )


# Delete blog


@blog_router.delete(
    "/{id}",
    response_model=blog_schemas.BlogEditResponse
)
async def delete_blog(
    blog_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    deleted_blog = await blog_service.delete_blog(
        blog_id,
        user,
        db
    )
    

    return blog_schemas.BlogEditResponse(
        status="success",
        message=f"Blog with ID {blog_id} deleted successfully",
        blog=deleted_blog
    )
