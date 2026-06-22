from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from src.api.deps import get_db, get_current_user
from src.infrastructure.database.models import User, NewsArticle

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/articles")
async def list_articles(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(NewsArticle)
        .order_by(NewsArticle.published_at.desc().nullslast())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    return result.scalars().all()


@router.get("/sentiment")
async def sentiment_trends(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(NewsArticle.source, NewsArticle.sentiment)
        .where(NewsArticle.sentiment.isnot(None))
    )
    rows = result.all()
    return [
        {"source": source, "sentiment": sentiment}
        for source, sentiment in rows
    ]
