
from datetime import datetime

from .base import Base

from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship
)

from sqlalchemy import DateTime, String, func


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False
    )

    username: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=True
    )

    password_hash: Mapped[bytes] = mapped_column(
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    blogs = relationship(
        "Blog",
        back_populates="user",
        cascade="all, delete-orphan")
