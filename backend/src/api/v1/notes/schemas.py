from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NoteCreate(BaseModel):
    title: str = Field(default="Untitled", max_length=500)
    content: Optional[str] = None
    content_json: Optional[dict] = None
    note_type: str = Field(default="document", pattern="^(document|canvas|whiteboard)$")
    icon: Optional[str] = None
    color: Optional[str] = None
    parent_id: Optional[str] = None


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = None
    content_json: Optional[dict] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    is_archived: Optional[bool] = None


class NoteResponse(BaseModel):
    id: str
    workspace_id: str
    author_id: str
    title: str
    content: Optional[str] = None
    content_json: Optional[dict] = None
    note_type: str
    icon: Optional[str] = None
    cover_url: Optional[str] = None
    color: Optional[str] = None
    is_published: bool
    is_archived: bool
    is_template: bool
    version: int
    parent_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NoteSummary(BaseModel):
    id: str
    title: str
    note_type: str
    icon: Optional[str] = None
    color: Optional[str] = None
    is_archived: bool
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = None


class TagResponse(BaseModel):
    id: str
    name: str
    color: Optional[str] = None

    class Config:
        from_attributes = True


class AISummarizeRequest(BaseModel):
    max_length: Optional[int] = 200


class AIRewriteRequest(BaseModel):
    tone: str = Field(default="professional", pattern="^(professional|casual|academic|creative)$")


class AITranslateRequest(BaseModel):
    target_language: str = Field(..., min_length=2, max_length=50)
