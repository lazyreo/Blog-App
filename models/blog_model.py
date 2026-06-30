
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


from .base import Base


class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        unique=True,
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    slug: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    content: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship("User", back_populates="blogs", lazy="raise")
