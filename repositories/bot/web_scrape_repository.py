
import html

from typing import Tuple, Union

from bs4 import BeautifulSoup

import httpx

from bs4 import XMLParsedAsHTMLWarning

import warnings

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.app.blog_repository import get_blog

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning, module="bs4"
                        )


def walk_json(obj, key):
    if isinstance(obj, dict):
        results = []
        if key in obj:
            results.append(obj[key])
        for value in obj.values():
            results.extend(walk_json(value, key))
        return results

    if isinstance(obj, list):
        results = []
        for item in obj:
            results.extend(walk_json(item, key))
        return results

    return []


async def get_crunchyrollnews(db: AsyncSession, client: httpx.AsyncClient) -> Union[Tuple[str, str], None]:
    try:
        response = await client.get(
            "https://cr-news-api-service.prd.crunchyrollsvc.com/v1/en-US/stories/search?category=Announcements,Latest+News,Latest+News&page_size=16&page=1"
        )
        response.raise_for_status()

        # Get story list

        data = response.json()
        stories = data.get("stories", [])

        for story in stories:
            slug = story["slug"]
            print(slug)

            article_url = (
                "https://cr-news-api-service.prd.crunchyrollsvc.com"
                f"/v1/en-US/stories?slug={slug}"
            )

            existing = await get_blog(
                db=db,
                user_id=2,
                url=article_url,
            )

            if existing:
                continue

            break
        else:
            logger.warning("No new articles found in Crunchyroll News!")
            return None

        article_response = await client.get(article_url)
        article_response.raise_for_status()
    except httpx.HTTPError:
        ...

    article_json = article_response.json()

    story_data = article_json.get("story")

    headline = (
        story_data
        .get("content", {})
        .get("headline", "")
    )

    text_parts = walk_json(
        story_data,
        "text"
    )

    contents = " ".join(text_parts)

    article = (f"Headline: {headline}\n"
               f"Slug: {slug}\n\n"
               f"Contents: {contents}")

    return article, article_url


async def get_animenewsnetwork(db: AsyncSession, client: httpx.AsyncClient) -> Union[Tuple[str, str], None]:
    try:
        response = await client.get(
            "https://www.animenewsnetwork.com/news/rss.xml"
        )
        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            features="xml"
        )
        titles = [title.get_text(strip=True)
                  for title in soup.find_all("title")]
        links = [link.get_text(strip=True)
                 for link in soup.find_all("guid")]

        for title, link in zip(titles[1:], links[1:]):
            print(title)
            url = await get_blog(
                db,
                user_id=1,
                url=link
            )
            if url is not None:
                continue

            break

        else:
            logger.warning("No new articles found in Anime News Network")
            return None

        response = await client.get(link)
        response.raise_for_status()
    except httpx.HTTPError:
        ...

    soup = BeautifulSoup(
        response.text,
        features="lxml"
    )

    p = soup.find_all("p")

    paragraphs = [html.unescape(paragraph.get_text(strip=True))
                  for paragraph in p]

    contents = "\n\n".join(paragraphs)

    article = f"Title: {title}\n\nContents: {contents}\n"
    return article, link


async def get_myanimelist(db: AsyncSession, client: httpx.AsyncClient) -> Union[Tuple[str, str], None]:
    header_tags = ["h1", "h2", "h3", "h4", "h5", "h6", ]

    try:

        response = await client.get(
            "https://myanimelist.net"
        )
        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            features="lxml"
        )

        path_to_links = soup.body.select(
            "div#myanimelist div.wrapper div#contentWrapper div.left-column article.widget-container.left div.widget.mxj.left div.widget-content a.ga-click.ga-impression"
        )

        links = []
        for link in path_to_links:
            links.append(link.get("href", ""))

        for link in links:
            print(link)
            url = await get_blog(
                db,
                user_id=3,
                url=link,
            )

            if url is not None:
                continue

            break

        else:
            logger.warning("No new articles found in My Anime List")
            return None

        response = await client.get(link)
        response.raise_for_status()
    except httpx.HTTPError:
        ...

    soup = BeautifulSoup(
        response.text,
        features="lxml"
    )

    body = soup.body

    if body is None:
        return None

    sections = body.find_all("section")

    text_content_list = []
    for section in sections:
        text_content_list.append("\n\n")
        if section.text:
            for texts in section.children:
                if texts.name in header_tags:
                    text_content_list.append("\n")
                text_content_list.append(f"{texts.text}\n")

    return "".join(text_content_list), link
