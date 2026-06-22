from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import uuid
from datetime import datetime, timezone

from src.api.deps import get_db, get_current_user
from src.infrastructure.database.models import (
    User, Task, TaskList, TaskSubtask, WorkspaceMember, PomodoroSession,
)
from src.api.v1.tasks.schemas import (
    TaskListCreate, TaskListResponse,
    TaskCreate, TaskUpdate, TaskResponse,
    TaskSubtaskCreate, TaskSubtaskUpdate, TaskSubtaskResponse,
    PomodoroStart,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


async def verify_workspace_access(workspace_id: str, user: User, db: AsyncSession):
    result = await db.execute(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == uuid.UUID(workspace_id),
            WorkspaceMember.user_id == user.id,
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Access denied")


# ── Task Lists ──────────────────────────────────────────────

@router.get("/lists", response_model=list[TaskListResponse])
async def list_task_lists(
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_workspace_access(workspace_id, user, db)
    result = await db.execute(
        select(TaskList)
        .where(TaskList.workspace_id == uuid.UUID(workspace_id))
        .order_by(TaskList.sort_order)
    )
    return result.scalars().all()


@router.post("/lists", response_model=TaskListResponse, status_code=201)
async def create_task_list(
    request: TaskListCreate,
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_workspace_access(workspace_id, user, db)
    task_list = TaskList(
        workspace_id=uuid.UUID(workspace_id),
        name=request.name,
        color=request.color,
        icon=request.icon,
        view_type=request.view_type,
    )
    db.add(task_list)
    await db.flush()
    return task_list


# ── Tasks ───────────────────────────────────────────────────

@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    workspace_id: str = Query(...),
    list_id: str = Query(None),
    status: str = Query(None),
    priority: str = Query(None),
    assignee_id: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_workspace_access(workspace_id, user, db)
    query = select(Task).join(TaskList).where(
        TaskList.workspace_id == uuid.UUID(workspace_id)
    )

    if list_id:
        query = query.where(Task.list_id == uuid.UUID(list_id))
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    if assignee_id:
        query = query.where(Task.assignee_id == uuid.UUID(assignee_id))

    query = query.order_by(Task.sort_order.nullslast(), Task.created_at.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    return result.scalars().all()


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    request: TaskCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = Task(
        list_id=uuid.UUID(request.list_id),
        title=request.title,
        description=request.description,
        status=request.status,
        priority=request.priority,
        labels=request.labels,
        assignee_id=uuid.UUID(request.assignee_id) if request.assignee_id else None,
        created_by=user.id,
        due_date=request.due_date,
        start_date=request.start_date,
        estimated_minutes=request.estimated_minutes,
        is_recurring=request.is_recurring,
        recurrence_rule=request.recurrence_rule,
    )
    db.add(task)
    await db.flush()
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await db.get(Task, uuid.UUID(task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    request: TaskUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await db.get(Task, uuid.UUID(task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    if task.status == "done" and not task.completed_at:
        task.completed_at = datetime.now(timezone.utc)
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await db.get(Task, uuid.UUID(task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)


@router.post("/{task_id}/move")
async def move_task(
    task_id: str,
    target_list_id: str = Query(...),
    new_sort_order: float = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await db.get(Task, uuid.UUID(task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.list_id = uuid.UUID(target_list_id)
    task.sort_order = new_sort_order
    return {"message": "Task moved successfully"}


# ── Subtasks ────────────────────────────────────────────────

@router.post("/{task_id}/subtasks", response_model=TaskSubtaskResponse, status_code=201)
async def create_subtask(
    task_id: str,
    request: TaskSubtaskCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await db.get(Task, uuid.UUID(task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    subtask = TaskSubtask(task_id=uuid.UUID(task_id), title=request.title)
    db.add(subtask)
    await db.flush()
    return subtask


@router.patch("/{task_id}/subtasks/{subtask_id}", response_model=TaskSubtaskResponse)
async def update_subtask(
    task_id: str,
    subtask_id: str,
    request: TaskSubtaskUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    subtask = await db.get(TaskSubtask, uuid.UUID(subtask_id))
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(subtask, key, value)
    return subtask


@router.delete("/{task_id}/subtasks/{subtask_id}", status_code=204)
async def delete_subtask(
    task_id: str,
    subtask_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    subtask = await db.get(TaskSubtask, uuid.UUID(subtask_id))
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    await db.delete(subtask)


# ── Pomodoro ────────────────────────────────────────────────

@router.post("/pomodoro/start")
async def start_pomodoro(
    request: PomodoroStart,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    session = PomodoroSession(
        user_id=user.id,
        task_id=uuid.UUID(request.task_id) if request.task_id else None,
        duration_minutes=request.duration_minutes,
        break_minutes=request.break_minutes,
        status="active",
        started_at=datetime.now(timezone.utc),
    )
    db.add(session)
    await db.flush()
    return {"id": str(session.id), "started_at": session.started_at, "duration_minutes": request.duration_minutes}
