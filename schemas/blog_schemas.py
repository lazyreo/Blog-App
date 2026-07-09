from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BlogPost(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str


class BlogUpdate(BaseModel):
    title: str | None = Field(min_length=1, max_length=100)
    content: str | None = None


class BlogResponse(BaseModel):
    id: int
    user_id: int
    title: str
    slug: str
    content: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class BlogEditResponse(BaseModel):
    status: str
    message: str
    blog: BlogResponse


class AIBlogResponse(BaseModel):
    title: str
    content: str
