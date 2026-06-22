from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from src.api.deps import get_db, get_current_user
from src.infrastructure.database.models import User, Document, WorkspaceMember

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("")
async def list_documents(
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Document).where(Document.workspace_id == uuid.UUID(workspace_id))
    )
    return result.scalars().all()


@router.post("/upload", status_code=201)
async def upload_document(
    workspace_id: str = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    content = await file.read()
    doc = Document(
        workspace_id=uuid.UUID(workspace_id),
        uploaded_by=user.id,
        original_name=file.filename or "untitled",
        mime_type=file.content_type or "application/octet-stream",
        size_bytes=len(content),
        storage_key=f"documents/{workspace_id}/{uuid.uuid4()}/{file.filename}",
    )
    db.add(doc)
    await db.flush()
    return doc


@router.delete("/{document_id}", status_code=204)
async def delete_document(
    document_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    doc = await db.get(Document, uuid.UUID(document_id))
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    await db.delete(doc)
