from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from src.api.deps import get_db, get_current_user
from src.infrastructure.database.models import User, PasswordVaultItem
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/passwords", tags=["passwords"])


class VaultItemCreate(BaseModel):
    name: str = Field(..., max_length=200)
    url: Optional[str] = None
    username: str
    password: str
    notes: Optional[str] = None
    category: Optional[str] = None
    tags: list[str] = []


class VaultItemResponse(BaseModel):
    id: str
    name: str
    url: Optional[str]
    category: Optional[str]
    tags: list
    strength_score: Optional[int]
    last_used_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class VaultItemDetail(VaultItemResponse):
    username: str
    password: str
    notes: Optional[str]


@router.get("/vault", response_model=list[VaultItemResponse])
async def list_vault(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(PasswordVaultItem).where(
            PasswordVaultItem.user_id == user.id
        ).order_by(PasswordVaultItem.created_at.desc())
    )
    return result.scalars().all()


@router.post("/vault", response_model=VaultItemResponse, status_code=201)
async def create_vault_item(
    request: VaultItemCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    item = PasswordVaultItem(
        user_id=user.id,
        name=request.name,
        url=request.url,
        username_encrypted=request.username,
        password_encrypted=request.password,
        notes_encrypted=request.notes,
        category=request.category,
        tags=request.tags,
        strength_score=len(request.password),
    )
    db.add(item)
    await db.flush()
    return item


@router.get("/vault/{item_id}", response_model=VaultItemDetail)
async def get_vault_item(
    item_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    item = await db.get(PasswordVaultItem, uuid.UUID(item_id))
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        **item.__dict__,
        "username": item.username_encrypted,
        "password": item.password_encrypted,
        "notes": item.notes_encrypted,
    }


@router.delete("/vault/{item_id}", status_code=204)
async def delete_vault_item(
    item_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    item = await db.get(PasswordVaultItem, uuid.UUID(item_id))
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(item)
