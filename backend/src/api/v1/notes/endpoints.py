from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
import uuid

from src.api.deps import get_db, get_current_user
from src.infrastructure.database.models import (
    User, Note, NoteTag, Workspace, WorkspaceMember,
)
from src.api.v1.notes.schemas import (
    NoteCreate, NoteUpdate, NoteResponse, NoteSummary,
    TagCreate, TagResponse,
    AISummarizeRequest, AIRewriteRequest, AITranslateRequest,
)

router = APIRouter(prefix="/notes", tags=["notes"])


async def verify_workspace_access(workspace_id: str, user: User, db: AsyncSession) -> Workspace:
    result = await db.execute(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == uuid.UUID(workspace_id),
            WorkspaceMember.user_id == user.id,
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to workspace",
        )
    ws = await db.get(Workspace, uuid.UUID(workspace_id))
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return ws


@router.get("", response_model=list[NoteSummary])
async def list_notes(
    workspace_id: str = Query(...),
    is_archived: bool = Query(False),
    search: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_workspace_access(workspace_id, user, db)

    query = select(Note).where(
        Note.workspace_id == uuid.UUID(workspace_id),
        Note.is_archived == is_archived,
    )

    if search:
        query = query.where(
            or_(
                Note.title.ilike(f"%{search}%"),
                Note.content_plain.ilike(f"%{search}%"),
            )
        )

    query = query.order_by(Note.updated_at.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    notes = result.scalars().all()
    return notes


@router.post("", response_model=NoteResponse, status_code=201)
async def create_note(
    request: NoteCreate,
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_workspace_access(workspace_id, user, db)

    note = Note(
        workspace_id=uuid.UUID(workspace_id),
        author_id=user.id,
        title=request.title,
        content=request.content,
        content_json=request.content_json,
        note_type=request.note_type,
        icon=request.icon,
        color=request.color,
        parent_id=uuid.UUID(request.parent_id) if request.parent_id else None,
    )
    db.add(note)
    await db.flush()
    return note


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    note = await db.get(Note, uuid.UUID(note_id))
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.patch("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: str,
    request: NoteUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    note = await db.get(Note, uuid.UUID(note_id))
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(note, key, value)
    note.version += 1

    return note


@router.delete("/{note_id}", status_code=204)
async def delete_note(
    note_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    note = await db.get(Note, uuid.UUID(note_id))
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.is_archived = True


@router.post("/{note_id}/restore", response_model=NoteResponse)
async def restore_note(
    note_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    note = await db.get(Note, uuid.UUID(note_id))
    if not note or not note.is_archived:
        raise HTTPException(status_code=404, detail="Archived note not found")
    note.is_archived = False
    return note


@router.post("/{note_id}/ai/summarize")
async def ai_summarize(
    note_id: str,
    request: AISummarizeRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    note = await db.get(Note, uuid.UUID(note_id))
    if not note or not note.content_plain:
        raise HTTPException(status_code=404, detail="Note not found or empty")
    return {"summary": f"[AI Summary would go here for: {note.title[:50]}...]"}


@router.post("/{note_id}/ai/rewrite")
async def ai_rewrite(
    note_id: str,
    request: AIRewriteRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    note = await db.get(Note, uuid.UUID(note_id))
    if not note or not note.content:
        raise HTTPException(status_code=404, detail="Note not found or empty")
    return {"rewritten": f"[AI Rewrite ({request.tone}) would go here]"}


@router.get("/{note_id}/backlinks")
async def get_backlinks(
    note_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    note = await db.get(Note, uuid.UUID(note_id))
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    # Backlinks are stored in content_json or content as [[wikilinks]]
    return {"backlinks": []}


# ─── Tags ──────────────────────────────────────────────────

@router.get("/tags", response_model=list[TagResponse])
async def list_tags(
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_workspace_access(workspace_id, user, db)
    result = await db.execute(
        select(NoteTag).where(NoteTag.workspace_id == uuid.UUID(workspace_id))
    )
    return result.scalars().all()


@router.post("/tags", response_model=TagResponse, status_code=201)
async def create_tag(
    request: TagCreate,
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_workspace_access(workspace_id, user, db)
    tag = NoteTag(
        workspace_id=uuid.UUID(workspace_id),
        name=request.name,
        color=request.color,
    )
    db.add(tag)
    await db.flush()
    return tag
