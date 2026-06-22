from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import uuid
from datetime import datetime, timezone

from src.api.deps import get_db, get_current_user
from src.infrastructure.database.models import (
    User, CalendarEvent, WorkspaceMember,
)
from src.api.v1.calendar.schemas import (
    CalendarEventCreate, CalendarEventUpdate, CalendarEventResponse,
    AIScheduleRequest,
)

router = APIRouter(prefix="/calendar", tags=["calendar"])


async def verify_workspace_access(workspace_id: str, user: User, db: AsyncSession):
    result = await db.execute(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == uuid.UUID(workspace_id),
            WorkspaceMember.user_id == user.id,
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Access denied")


@router.get("/events", response_model=list[CalendarEventResponse])
async def list_events(
    workspace_id: str = Query(...),
    start_date: str = Query(None),
    end_date: str = Query(None),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_workspace_access(workspace_id, user, db)
    query = select(CalendarEvent).where(
        CalendarEvent.workspace_id == uuid.UUID(workspace_id)
    )

    if start_date:
        query = query.where(CalendarEvent.start_time >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.where(CalendarEvent.end_time <= datetime.fromisoformat(end_date))

    query = query.order_by(CalendarEvent.start_time)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/events", response_model=CalendarEventResponse, status_code=201)
async def create_event(
    request: CalendarEventCreate,
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_workspace_access(workspace_id, user, db)
    event = CalendarEvent(
        workspace_id=uuid.UUID(workspace_id),
        creator_id=user.id,
        title=request.title,
        description=request.description,
        location=request.location,
        is_all_day=request.is_all_day,
        start_time=request.start_time,
        end_time=request.end_time,
        timezone=request.timezone,
        recurrence_rule=request.recurrence_rule,
    )
    db.add(event)
    await db.flush()
    return event


@router.get("/events/{event_id}", response_model=CalendarEventResponse)
async def get_event(
    event_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    event = await db.get(CalendarEvent, uuid.UUID(event_id))
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.patch("/events/{event_id}", response_model=CalendarEventResponse)
async def update_event(
    event_id: str,
    request: CalendarEventUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    event = await db.get(CalendarEvent, uuid.UUID(event_id))
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(event, key, value)
    return event


@router.delete("/events/{event_id}", status_code=204)
async def delete_event(
    event_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    event = await db.get(CalendarEvent, uuid.UUID(event_id))
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    await db.delete(event)


@router.post("/ai/schedule")
async def ai_schedule(
    request: AIScheduleRequest,
    user: User = Depends(get_current_user),
):
    # AI-powered scheduling assistant
    return {
        "suggestions": [
            {
                "date": "2026-06-23",
                "start_time": "10:00",
                "end_time": "10:30",
                "confidence": 0.85,
            }
        ]
    }
