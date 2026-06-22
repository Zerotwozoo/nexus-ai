from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from datetime import datetime, timezone

from src.api.deps import get_db, get_current_user
from src.infrastructure.database.models import (
    User, AutomationWorkflow, WorkspaceMember,
)
from src.api.v1.automation.schemas import *

router = APIRouter(prefix="/automation", tags=["automation"])


@router.get("/workflows", response_model=list[WorkflowResponse])
async def list_workflows(
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(AutomationWorkflow).where(
            AutomationWorkflow.workspace_id == uuid.UUID(workspace_id)
        ).order_by(AutomationWorkflow.created_at.desc())
    )
    return result.scalars().all()


@router.post("/workflows", response_model=WorkflowResponse, status_code=201)
async def create_workflow(
    request: WorkflowCreate,
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    workflow = AutomationWorkflow(
        workspace_id=uuid.UUID(workspace_id),
        created_by=user.id,
        name=request.name,
        description=request.description,
        trigger_type=request.trigger_type,
        trigger_config=request.trigger_config,
        steps=request.steps,
    )
    db.add(workflow)
    await db.flush()
    return workflow


@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    workflow = await db.get(AutomationWorkflow, uuid.UUID(workflow_id))
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@router.patch("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: str,
    request: WorkflowUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    workflow = await db.get(AutomationWorkflow, uuid.UUID(workflow_id))
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(workflow, key, value)
    return workflow


@router.delete("/workflows/{workflow_id}", status_code=204)
async def delete_workflow(
    workflow_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    workflow = await db.get(AutomationWorkflow, uuid.UUID(workflow_id))
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    await db.delete(workflow)


@router.post("/workflows/{workflow_id}/trigger")
async def trigger_workflow(
    workflow_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    workflow = await db.get(AutomationWorkflow, uuid.UUID(workflow_id))
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflow.last_run_at = datetime.now(timezone.utc)
    return {"message": f"Workflow '{workflow.name}' triggered", "steps": len(workflow.steps)}
