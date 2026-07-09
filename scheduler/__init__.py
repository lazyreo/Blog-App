from __future__ import annotations
from .celery_app import celery_app
from .tasks.post_ai_blog import post_ai_blogs

__all__ = [
    "celery_app",
    "post_ai_blogs"
]
