from celery import Celery
from loguru import logger
from app.config.settings import settings
from celery.schedules import crontab

celery_app = Celery(
    "blog_worker",
    broker=settings.REDIS_BROKER,
    backend=settings.REDIS_BROKER,
)


def _setup_celery():

    logger.info("Celery app starting...")

    celery_app.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True,
    )

    celery_app.conf.beat_schedule = {
        "post-ai-blogs-every-1-hour": {
            "task": "scheduler.tasks.post_ai_blog",
            "schedule": crontab(hour=1, minute=0)
        }
    }

    logger.info("Celery app started")


async def start_celery():
    _setup_celery()
    celery_app.autodiscover_tasks("scheduler")
