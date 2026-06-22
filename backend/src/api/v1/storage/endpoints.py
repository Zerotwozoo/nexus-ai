from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from src.api.deps import get_db, get_current_user
from src.infrastructure.database.models import User, StorageFile, WorkspaceMember

router = APIRouter(prefix="/storage", tags=["storage"])


@router.get("/files")
async def list_files(
    workspace_id: str = Query(...),
    parent_id: str = Query(None),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(StorageFile).where(
        StorageFile.workspace_id == uuid.UUID(workspace_id)
    )
    if parent_id:
        query = query.where(StorageFile.parent_id == uuid.UUID(parent_id))
    else:
        query = query.where(StorageFile.parent_id.is_(None))
    query = query.order_by(StorageFile.is_folder.desc(), StorageFile.name)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/files/upload", status_code=201)
async def upload_file(
    workspace_id: str = Query(...),
    file: UploadFile = File(...),
    parent_id: str = Query(None),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    content = await file.read()
    storage_file = StorageFile(
        workspace_id=uuid.UUID(workspace_id),
        uploaded_by=user.id,
        name=file.filename or "untitled",
        storage_key=f"storage/{workspace_id}/{uuid.uuid4()}/{file.filename}",
        mime_type=file.content_type or "application/octet-stream",
        size_bytes=len(content),
        parent_id=uuid.UUID(parent_id) if parent_id else None,
    )
    db.add(storage_file)
    await db.flush()
    return storage_file


@router.post("/files/folder", status_code=201)
async def create_folder(
    workspace_id: str = Query(...),
    name: str = Query(..., min_length=1),
    parent_id: str = Query(None),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    folder = StorageFile(
        workspace_id=uuid.UUID(workspace_id),
        uploaded_by=user.id,
        name=name,
        storage_key=f"storage/{workspace_id}/{uuid.uuid4()}/{name}",
        is_folder=True,
        parent_id=uuid.UUID(parent_id) if parent_id else None,
    )
    db.add(folder)
    await db.flush()
    return folder


@router.delete("/files/{file_id}", status_code=204)
async def delete_file(
    file_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    file = await db.get(StorageFile, uuid.UUID(file_id))
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    await db.delete(file)
