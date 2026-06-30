
from models.blog_model import Blog

from models.user_model import User

from schemas import blog_schemas

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.app import blog_repository

from errors.exceptions import BlogIDNotFoundException

# Post blog


async def post_blog(
    blog: blog_schemas.BlogPost,
    user: User,
    db: AsyncSession
):

    return await blog_repository.post_blog(
        blog,
        user,
        db
    )


# Read all blogs


async def get_blogs(
    db: AsyncSession,
    page: int = 1,
    blogs_per_page: int = 10
) -> list[Blog]:

    return await blog_repository.get_blogs(
        db,
        page=page,
        blogs_per_page=blogs_per_page
    )


# Read a blog

async def get_blog(
    blog_id: int,
    db: AsyncSession
) -> Blog:

    blog =  await blog_repository.get_blog(
        db,
        blog_id,
    )

    if blog is None:
        raise BlogIDNotFoundException(blog_id)

    return blog

# Read blogs of a user


async def get_blogs_of_user(
    user: User,
    db: AsyncSession
):

    return await blog_repository.get_blogs_of_user(user, db)

# Update a blog


async def update_blog(
    blog_id: int,
    updated_blog: blog_schemas.BlogPost,
    user: User,
    db: AsyncSession,
):
    updated_blog =  await blog_repository.update_blog(
        blog_id,
        updated_blog,
        user,
        db
    )
    
    if updated_blog is None:
        raise BlogIDNotFoundException(blog_id)
    
    return updated_blog

# Delete a blog


async def delete_blog(
    blog_id: int,
    user: User,
    db: AsyncSession
):

    deleted_blog = await blog_repository.delete_blog(
        blog_id,
        user,
        db
    )
    
    if deleted_blog is None:
        raise BlogIDNotFoundException(blog_id)
    
    return deleted_blog


