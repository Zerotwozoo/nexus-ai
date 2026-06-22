from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
import uuid

from src.api.deps import get_db, get_current_user
from src.infrastructure.database.models import (
    User, Workspace, WorkspaceMember, Comment, ActivityLog,
)
from src.api.v1.collaboration.schemas import (
    WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse,
    WorkspaceMemberResponse, InviteMemberRequest, UpdateMemberRoleRequest,
    CommentCreate, CommentUpdate, CommentResponse,
    ActivityLogResponse,
)
from src.infrastructure.auth.jwt import hash_password

router = APIRouter(tags=["collaboration"])


# ── Workspaces ──────────────────────────────────────────────

@router.get("/workspaces", response_model=list[WorkspaceResponse])
async def list_workspaces(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Workspace).join(WorkspaceMember).where(
            WorkspaceMember.user_id == user.id,
            WorkspaceMember.role.in_(["owner", "admin", "member"]),
        )
    )
    return result.scalars().all()


@router.post("/workspaces", response_model=WorkspaceResponse, status_code=201)
async def create_workspace(
    request: WorkspaceCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    existing = await db.execute(
        select(Workspace).where(Workspace.slug == request.slug)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Slug already taken")

    workspace = Workspace(
        owner_id=user.id,
        name=request.name,
        slug=request.slug,
    )
    db.add(workspace)
    await db.flush()

    member = WorkspaceMember(
        workspace_id=workspace.id,
        user_id=user.id,
        role="owner",
    )
    db.add(member)
    return workspace


@router.get("/workspaces/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    workspace = await db.get(Workspace, uuid.UUID(workspace_id))
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace


@router.patch("/workspaces/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(
    workspace_id: str,
    request: WorkspaceUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    workspace = await db.get(Workspace, uuid.UUID(workspace_id))
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    if workspace.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Only owner can update workspace")
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(workspace, key, value)
    return workspace


@router.get("/workspaces/{workspace_id}/members", response_model=list[WorkspaceMemberResponse])
async def list_members(
    workspace_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == uuid.UUID(workspace_id)
        )
    )
    return result.scalars().all()


@router.post("/workspaces/{workspace_id}/members", response_model=WorkspaceMemberResponse, status_code=201)
async def invite_member(
    workspace_id: str,
    request: InviteMemberRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    workspace = await db.get(Workspace, uuid.UUID(workspace_id))
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    target_user = await db.execute(
        select(User).where(User.email == request.email)
    )
    target = target_user.scalar_one_or_none()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    existing = await db.execute(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == uuid.UUID(workspace_id),
            WorkspaceMember.user_id == target.id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="User already member")

    member = WorkspaceMember(
        workspace_id=uuid.UUID(workspace_id),
        user_id=target.id,
        role=request.role,
    )
    db.add(member)
    await db.flush()
    return member


@router.patch("/workspaces/{workspace_id}/members/{member_id}", response_model=WorkspaceMemberResponse)
async def update_member_role(
    workspace_id: str,
    member_id: str,
    request: UpdateMemberRoleRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    member = await db.get(WorkspaceMember, uuid.UUID(member_id))
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    member.role = request.role
    return member


@router.delete("/workspaces/{workspace_id}/members/{member_id}", status_code=204)
async def remove_member(
    workspace_id: str,
    member_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    member = await db.get(WorkspaceMember, uuid.UUID(member_id))
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    await db.delete(member)


# ── Comments ────────────────────────────────────────────────

@router.get("/comments", response_model=list[CommentResponse])
async def list_comments(
    resource_type: str = Query(...),
    resource_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Comment).where(
            Comment.resource_type == resource_type,
            Comment.resource_id == uuid.UUID(resource_id),
        ).order_by(Comment.created_at)
    )
    return result.scalars().all()


@router.post("/comments", response_model=CommentResponse, status_code=201)
async def create_comment(
    request: CommentCreate,
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    comment = Comment(
        workspace_id=uuid.UUID(workspace_id),
        author_id=user.id,
        resource_type=request.resource_type,
        resource_id=uuid.UUID(request.resource_id),
        parent_id=uuid.UUID(request.parent_id) if request.parent_id else None,
        content=request.content,
    )
    db.add(comment)
    await db.flush()
    return comment


# ── Activity ────────────────────────────────────────────────

@router.get("/activity", response_model=list[ActivityLogResponse])
async def list_activity(
    workspace_id: str = Query(...),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(ActivityLog)
        .where(ActivityLog.workspace_id == uuid.UUID(workspace_id))
        .order_by(ActivityLog.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    result = await db.execute(query)
    return result.scalars().all()
