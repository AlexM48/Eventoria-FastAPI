from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class EventCreate(BaseModel):
    title: str
    description: str


class EventResponse(BaseModel):
    id: int
    title: str
    description: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedEvents(BaseModel):
    items: list[EventResponse]
    total: int
    page: int
    size: int


class EventFilter(BaseModel):
    title: str | None = None



