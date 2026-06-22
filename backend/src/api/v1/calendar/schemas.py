from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CalendarEventCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    description: Optional[str] = None
    location: Optional[str] = None
    is_all_day: bool = False
    start_time: datetime
    end_time: datetime
    timezone: str = "UTC"
    recurrence_rule: Optional[str] = None
    attendees: list[str] = []


class CalendarEventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    is_all_day: Optional[bool] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    timezone: Optional[str] = None
    recurrence_rule: Optional[str] = None


class CalendarEventResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    location: Optional[str]
    is_all_day: bool
    start_time: datetime
    end_time: datetime
    timezone: str
    recurrence_rule: Optional[str]
    creator_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AIScheduleRequest(BaseModel):
    title: str
    duration_minutes: int = 30
    preferred_days: list[str] = []
    preferred_time_start: Optional[str] = None
    preferred_time_end: Optional[str] = None
    notes: Optional[str] = None
