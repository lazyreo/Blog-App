

from datetime import datetime

from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship
)

from sqlalchemy import (
    DateTime,
    String,
    Text,
    ForeignKey,
    func
)

from .user_model import User

from .base import Base


class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    url: Mapped[str | None] = mapped_column(
        String(500),
        unique=True,
        index=True,
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="blogs"
    )
