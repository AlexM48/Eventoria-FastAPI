from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Index

class Event(Base):

    __tablename__ = "events"

    __table_args__ = (
        Index("ix_events_owner_id", "owner_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    # ← Primary key

    title: Mapped[str] = mapped_column(String(255))
    # ← Название события

    description: Mapped[str]
    # ← Описание

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner = relationship("User")

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )