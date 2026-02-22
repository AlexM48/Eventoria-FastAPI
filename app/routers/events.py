from fastapi import APIRouter, Depends, Query

from app.schemas.event import (
    EventCreate,
    EventResponse,
    PaginatedEvents
)

from app.services.event_services import (
    create_event,
    get_my_events
)
# ← бизнес логика
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.core.deps import get_current_user

from app.models.user import User

from app.schemas.event import EventCreate, EventResponse, EventUpdate

from app.services.event_services import (
    create_event,
    get_my_events,
    get_event,
    update_event,
    patch_event,
    delete_event
)



router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.post("", response_model=EventResponse)
async def create_event_endpoint(
    data: EventCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    event = await create_event(
        db=db,
        user_id=user.id,
        data=data
    )

    return event



@router.get("/my", response_model=PaginatedEvents)
async def get_my_events_endpoint(
    page: int = Query(1, ge=1),
    size: int = Query(10, le=100),
    title: str | None = None,
    sort_by: str = Query("created_at"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    events, total = await get_my_events(
        db=db,
        user_id=user.id,
        page=page,
        size=size,
        title=title,
        sort_by=sort_by,
        order=order
    )

    return {
        "items": events,
        "total": total,
        "page": page,
        "size": size
    }


@router.post("", response_model=EventResponse)
async def create_event_endpoint(
    data: EventCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return await create_event(db, user.id, data)


@router.get("/{event_id}", response_model=EventResponse)
async def get_event_endpoint(
    event_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return await get_event(db, event_id, user.id)


@router.put("/{event_id}", response_model=EventResponse)
async def update_event_endpoint(
    event_id: int,
    data: EventCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return await update_event(db, event_id, user.id, data)


@router.patch("/{event_id}", response_model=EventResponse)
async def patch_event_endpoint(
    event_id: int,
    data: EventUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return await patch_event(db, event_id, user.id, data)


@router.delete("/{event_id}")
async def delete_event_endpoint(
    event_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    await delete_event(db, event_id, user.id)
    return {"status": "deleted"}
