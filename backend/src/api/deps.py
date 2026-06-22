from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.infrastructure.auth.dependencies import get_current_user
from src.infrastructure.database.models import User

__all__ = ["get_db", "get_current_user"]
