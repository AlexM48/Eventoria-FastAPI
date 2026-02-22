
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event

from app.schemas.event import EventCreate
from sqlalchemy import select, func, asc, desc

from fastapi import HTTPException


async def create_event(
    db: AsyncSession,
    user_id: int,
    data: EventCreate
):

    event = Event(
        title=data.title,
        description=data.description,
        owner_id=user_id
    )

    db.add(event)
    await db.commit()
    await db.refresh(event)

    return event



async def get_my_events(
    db: AsyncSession,
    user_id: int,
    page: int,
    size: int,
    title: str | None,
    sort_by: str = "created_at",
    order: str = "desc"
):
    #разрешенные поля сортировки
    allowed_sort_fields = {
        "created_at": Event.created_at,
        "title": Event.title,
    }
    #если передано неразрешенное поле
    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field. Allowed: {list(allowed_sort_fields.keys())}"
        )
    #получаем колонку
    sort_column = allowed_sort_fields[sort_by]

    query = select(Event).where(Event.owner_id == user_id)

    #порядок сортировки
    if order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    if title:
        query = query.where(Event.title.ilike(f"%{title}%"))


    total = await db.scalar(select(func.count()).select_from(query.subquery()))


    query = query.offset((page - 1) * size).limit(size)


    result = await db.execute(query)
    events = result.scalars().all()
    return events, total


async def get_event(db, event_id: int, user_id: int):

    query = select(Event).where(Event.id == event_id)


    result = await db.execute(query)
    event = result.scalar_one_or_none()


    if not event:
        raise HTTPException(404, "Event not found")


    if event.owner_id != user_id:
        raise HTTPException(403, "Not your event")


    return event


async def update_event(db, event_id: int, user_id: int, data):

    event = await get_event(db, event_id, user_id)

    event.title = data.title
    event.description = data.description

    await db.commit()
    await db.refresh(event)

    return event


async def patch_event(db, event_id: int, user_id: int, data):

    event = await get_event(db, event_id, user_id)

    if data.title is not None:
        event.title = data.title

    if data.description is not None:
        event.description = data.description

    await db.commit()
    await db.refresh(event)

    return event


async def delete_event(db, event_id: int, user_id: int):

    event = await get_event(db, event_id, user_id)

    await db.delete(event)
    await db.commit()

    return True
