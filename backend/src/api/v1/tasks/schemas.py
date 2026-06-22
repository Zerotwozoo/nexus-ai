from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskListCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    color: Optional[str] = None
    icon: Optional[str] = None
    view_type: str = Field(default="kanban", pattern="^(kanban|calendar|list|timeline)$")


class TaskListResponse(BaseModel):
    id: str
    name: str
    color: Optional[str]
    icon: Optional[str]
    view_type: str
    sort_order: int

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    list_id: str
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    status: str = Field(default="backlog", pattern="^(backlog|todo|in_progress|review|done)$")
    priority: str = Field(default="medium", pattern="^(urgent|high|medium|low)$")
    labels: list[str] = []
    assignee_id: Optional[str] = None
    due_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    estimated_minutes: Optional[int] = None
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    labels: Optional[list[str]] = None
    assignee_id: Optional[str] = None
    due_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    estimated_minutes: Optional[int] = None


class TaskResponse(BaseModel):
    id: str
    list_id: str
    assignee_id: Optional[str]
    created_by: Optional[str]
    title: str
    description: Optional[str]
    status: str
    priority: str
    labels: list
    due_date: Optional[datetime]
    start_date: Optional[datetime]
    estimated_minutes: Optional[int]
    sort_order: Optional[float]
    is_recurring: bool
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskSubtaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)


class TaskSubtaskUpdate(BaseModel):
    title: Optional[str] = None
    is_completed: Optional[bool] = None


class TaskSubtaskResponse(BaseModel):
    id: str
    task_id: str
    title: str
    is_completed: bool
    sort_order: int

    class Config:
        from_attributes = True


class PomodoroStart(BaseModel):
    task_id: Optional[str] = None
    duration_minutes: int = Field(default=25, ge=1, le=120)
    break_minutes: int = Field(default=5, ge=1, le=30)
