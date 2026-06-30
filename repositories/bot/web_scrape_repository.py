
import html

from bs4 import BeautifulSoup

import asyncio

import httpx

from app.config.celery_app import celery_app

from bs4 import XMLParsedAsHTMLWarning

import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning, module="bs4"
                        )


def walk_json(obj, key):
    results = []

    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                results.append(v)

            results.extend(walk_json(v, key))

    elif isinstance(obj, list):
        for item in obj:
            results.extend(walk_json(item, key))

    return results


async def fetch(
    url: str,
    client: httpx.AsyncClient
):
    response = await client.get(url)

    response.raise_for_status()

    return response


async def fetch_many(urls: list[str] | str):
    headers = {
        "User-Agent": (
            "Mozilla/5.0"
        )
    }

    async with httpx.AsyncClient(
        headers=headers,
        follow_redirects=True,
        timeout=30,
    ) as client:

        tasks = [
            fetch(url, client) for url in urls
        ]

        return await asyncio.gather(*tasks)


def parse_html(response_txt: str):
    soup = BeautifulSoup(
        response_txt,
        "html.parser"
    )

    return soup


@celery_app.task
async def scrape_article(url: str):
    headers = {
        "User-Agent": (
            "Mozilla/5.0"
        )
    }

    async with httpx.AsyncClient(
        headers=headers,
        follow_redirects=True,
        timeout=30,
    ) as client:

        response = await client.get(url)

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    title = ""

    if soup.title:
        title = soup.title.get_text(strip=True)

    return {
        "url": url,
        "title": title,
    }


async def get_crunchyrollnews():

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient(
        headers=headers,
        follow_redirects=True,
        timeout=30
    ) as client:

        # Get story list
        response = await client.get(
            "https://cr-news-api-service.prd.crunchyrollsvc.com/v1/en-US/stories/search?category=Announcements,Latest+News,Latest+News&page_size=16&page=1"
        )

        data = response.json()

        story = data.get("stories", [])[0]

        slug = story.get("slug")

        article_url = (
            "https://cr-news-api-service.prd.crunchyrollsvc.com"
            f"/v1/en-US/stories?slug={slug}"
        )

        article_response = await client.get(article_url)

        article_json = article_response.json()

        story_data = article_json["story"]

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

        article = ({
            "headline": headline,
            "slug": slug,
            "content": contents
        })

    return article


async def get_animenewsnetwork():

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient(
        headers=headers,
        follow_redirects=True,
        timeout=30
    ) as client:

        response = await client.get(
            "https://www.animenewsnetwork.com/news/rss.xml"
        )

        soup = BeautifulSoup(
            response.text,
            features="lxml"
        )

        link = soup.find_all("guid", limit=2)[1].get_text(strip=True)

        title = soup.find_all("title", limit=2)[1].get_text(strip=True)

        response = await client.get(link)

        soup = BeautifulSoup(
            response.text,
            features="lxml"
        )

        p = soup.find_all("p")

        paragraphs = [html.unescape(paragraph.get_text(strip=True))
                      for paragraph in p]

        data = {
            "title": title,
            "paragraphs": paragraphs
        }

    return data


async def get_myanimelist():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient(
        headers=headers,
        follow_redirects=True,
        timeout=30
    ) as client:

        response = await client.get(
            "https://myanimelist.net"
        )

        soup = BeautifulSoup(
            response.text,
            features="lxml"
        )

        link = soup.body.select_one(
            "div#myanimelist div.wrapper div#contentWrapper div.left-column article.widget-container.left div.widget.mxj.left div.widget-content a.ga-click.ga-impression"
        ).get("href")
