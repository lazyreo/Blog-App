
from sqlalchemy import (
    delete,
    exists,
    or_,
    select
)

from slugify import slugify

from sqlalchemy.ext.asyncio import AsyncSession

from models.user_model import User
from models.blog_model import Blog

from schemas.blog_schemas import BlogPost, BlogUpdate


# Generate slug


async def generate_slug(
    title: str,
    db: AsyncSession
) -> str:
    base_slug = slugify(title)

    query = select(Blog.slug).where(
        or_(
            Blog.slug == base_slug,
            Blog.slug.like(f"{base_slug}-%")
        )
    )

    result = await db.scalars(query)
    existing = set(result.all())

    if base_slug not in existing:
        return base_slug

    counter = 2

    while True:
        candidate = f"{base_slug}-{counter}"

        if candidate not in existing:
            return candidate

        counter += 1


async def is_slug_exists(db: AsyncSession, title: str):
    base_slug = slugify(title)

    is_exists = (await db.execute(select(exists().where(Blog.slug == base_slug)))).scalar_one_or_none()

    return is_exists

# Read all blogs


async def get_blogs(
    db: AsyncSession,
    page: int = 1,
    blogs_per_page: int = 10
) -> list[Blog]:

    offset = (page - 1) * blogs_per_page

    limit = blogs_per_page

    result = await db.execute(
        select(Blog)
        .order_by(Blog.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    return list(result.scalars().all())

# Read a blog with ID / slug


async def get_blog(
    db: AsyncSession,
    blog_id: int | None = None,
    user_id: int | None = None,
    slug: str | None = None,
    url: str | None = None

) -> Blog | None:

    conditions = []

    if blog_id is not None:
        conditions.append(Blog.id == blog_id)

    if user_id is not None:
        conditions.append(Blog.user_id == user_id)

    if slug is not None:
        conditions.append(Blog.slug == slug)

    if url is not None:
        conditions.append(Blog.url == url)

    else:
        return None

    result = await db.execute(
        select(
            Blog
        ).where(
            *conditions
        )
    )

    return result.scalar_one_or_none()

# Read blogs of user


async def get_blogs_of_user(
    user: User,
    db: AsyncSession
) -> list[Blog]:

    result = await db.execute(
        select(Blog)
        .where(Blog.user_id == user.id)
    )

    return result.scalars().all()


# Post a blog


async def post_blog(
    blog: BlogPost,
    user: User,
    db: AsyncSession
) -> Blog:
    slug = await generate_slug(
        blog.title,
        db
    )

    post = Blog(
        user_id=user.id,
        title=blog.title,
        slug=slug,
        content=blog.content
    )

    db.add(post)

    await db.commit()

    await db.refresh(post)

    return post


# Update a blog's content / title


async def update_blog(
    blog_id: int,
    updated_blog: BlogUpdate,
    user: User,
    db: AsyncSession,
) -> Blog | None:
    result = await db.execute(
        select(Blog)
        .where(
            Blog.id == blog_id,
            Blog.user_id == user.id
        )
    )

    existing_blog = result.scalar_one_or_none()

    if existing_blog is None:
        return None

    title: str | None = updated_blog.title
    content: str | None = updated_blog.content

    if title:
        existing_blog.title = title

    if content:
        existing_blog.content = content

    elif not title and not content:
        return None

    await db.commit()

    await db.refresh(existing_blog)

    return existing_blog


# Delete a blog


async def delete_blog(
    blog_id: int,
    user: User,
    db: AsyncSession,
) -> Blog | None:

    result = await db.execute(
        delete(Blog).where(
            Blog.id == blog_id,
            Blog.user_id == user.id,
        ).returning(Blog)
    )

    deleted_blog = result.scalar_one_or_none()

    if deleted_blog is None:
        return None

    await db.commit()

    return deleted_blog
