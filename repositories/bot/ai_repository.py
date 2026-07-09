
from typing import Union

from httpx import AsyncClient

from loguru import logger

from app.config.llm_client import (
    model,
    client
)

from bot.client import ARTICLE_REPHRASE_PROMPT

from models import blog_model

from google.genai import types


from sqlalchemy.ext.asyncio import AsyncSession

from repositories.app.blog_repository import generate_slug

from schemas.blog_schemas import AIBlogResponse

from .web_scrape_repository import get_animenewsnetwork, get_crunchyrollnews, get_myanimelist

from google.genai.types import GenerateContentResponse
# Get an AI response


async def get_ai_response_async(
    contents: str,
    config: dict,
    model: str = model,
    stream: bool = False
) -> GenerateContentResponse:
    if not stream:
        response: GenerateContentResponse = await client.aio.models.generate_content(
            model=model,
            contents=contents,
            config=config
        )
        return response

    else:
        response: GenerateContentResponse = await client.aio.models.generate_content_stream(
            model=model,
            contents=contents,
            config=config
        )
        return response


async def article_rephraser(
    article: str
) -> AIBlogResponse:

    parts = [
        types.Part.from_text(text=article),
    ]

    contents = types.Content(
        role="user",
        parts=parts
    )

    config = types.GenerateContentConfig(
        system_instruction=ARTICLE_REPHRASE_PROMPT,
        temperature=0.7,
        response_mime_type="application/json",
        response_schema=AIBlogResponse
    )

    response = await get_ai_response_async(
        contents=contents,
        config=config
    )

    return response.parsed


async def post_ai_article(
    db: AsyncSession,
    client: AsyncClient,
    bot_id: Union[1, 2, 3, None] = None,
) -> blog_model.Blog:

    if bot_id is None or bot_id == 1:
        result = await get_animenewsnetwork(db, client)

    elif bot_id == 2:
        result = await get_crunchyrollnews(db, client)

    elif bot_id == 3:
        result = await get_myanimelist(db, client)

    else:
        logger.error("Unable to recognise ID")
        raise ValueError

    if result is None:
        return None

    article = result[0]
    url = result[1]

    # Generate AI Article
    response: AIBlogResponse = await article_rephraser(article)

    title = response.title
    content = response.content

    slug = await generate_slug(title, db)

    blog = blog_model.Blog(
        user_id=bot_id,
        title=title,
        slug=slug,
        content=content,
        url=url,
    )

    db.add(blog)

    return blog
