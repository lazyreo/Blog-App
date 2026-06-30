
from app.config.llm_client import (
    model,
    client
)

from models import blog_model


from sqlalchemy.ext.asyncio import AsyncSession
# Get an AI response
async def get_ai_response(
    contents,
    config,
    model=model,
    stream=False
):
    if not stream:
        response = await client.models.generate_content(
            model=model,
            contents=contents,
            config=config
        )
        return response
    
    elif stream:
        response = await client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=config
        )
        return response


async def article_rephraser(
    article: str
):
    contents = [
        {
            "type": "text",
            "text": article
        }
    ]

    config = {
        "temperature": 0.7,
        "max_output_tokens": 500
    }

    response = await get_ai_response(
        contents,
        config
    )

    return response

async def post_ai_article(
    db: AsyncSession,
    title: str,
    content: str,
    user_id: int
):
    blog = blog_model.Blog(title=title, content=content, user_id=user_id)

    db.add(blog)
    await db.commit()  
    await db.refresh(blog)
    
    return blog