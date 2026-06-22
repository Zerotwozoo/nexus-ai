from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentResponse(BaseModel):
    id: str
    workspace_id: str
    uploaded_by: Optional[str]
    original_name: str
    mime_type: Optional[str]
    size_bytes: Optional[int]
    page_count: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
