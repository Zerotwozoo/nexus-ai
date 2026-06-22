from fastapi import APIRouter
from src.api.v1.auth.endpoints import router as auth_router
from src.api.v1.notes.endpoints import router as notes_router
from src.api.v1.tasks.endpoints import router as tasks_router
from src.api.v1.calendar.endpoints import router as calendar_router
from src.api.v1.collaboration.endpoints import router as collaboration_router
from src.api.v1.documents.endpoints import router as documents_router
from src.api.v1.finance.endpoints import router as finance_router
from src.api.v1.trading.endpoints import router as trading_router
from src.api.v1.automation.endpoints import router as automation_router
from src.api.v1.passwords.endpoints import router as passwords_router
from src.api.v1.news.endpoints import router as news_router
from src.api.v1.storage.endpoints import router as storage_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(notes_router)
api_router.include_router(tasks_router)
api_router.include_router(calendar_router)
api_router.include_router(collaboration_router)
api_router.include_router(documents_router)
api_router.include_router(finance_router)
api_router.include_router(trading_router)
api_router.include_router(automation_router)
api_router.include_router(passwords_router)
api_router.include_router(news_router)
api_router.include_router(storage_router)
