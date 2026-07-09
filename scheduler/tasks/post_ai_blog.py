import asyncio

from httpx import AsyncClient

from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database import with_session

from repositories.bot.ai_repository import post_ai_article

from scheduler.celery_app import celery_app


@with_session
async def post_ai_blogs_async(db: AsyncSession):

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    async with AsyncClient(
        headers=headers,
        timeout=30,
        follow_redirects=True,
    ) as client:

        for bot_id in range(1, 4):

            try:

                logger.info("Posting an article...")

                is_posted_successfully = await post_ai_article(
                    db=db,
                    client=client,
                    bot_id=bot_id
                )

                if not is_posted_successfully:
                    continue

                logger.info("Successfully posted an article!")

                await asyncio.sleep(60)

            except Exception:
                logger.exception("Failed to post AI article.")
    return


@celery_app.task
def post_ai_blogs():
    asyncio.run(post_ai_blogs_async())
