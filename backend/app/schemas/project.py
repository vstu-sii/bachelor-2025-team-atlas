from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    DRAFT = "draft"
    UPLOADED = "uploaded"
    PARSING = "parsing"
    PARSED = "parsed"
    OPTIMIZING = "optimizing"
    READY = "ready"
    EXPORTED = "exported"
    ARCHIVED = "archived"

class ProjectVisibility(str, Enum):
    PRIVATE = "private"
    TEAM = "team"
    PUBLIC = "public"

class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    industry: Optional[str] = None
    language: str = "ru"
    visibility: Optional[ProjectVisibility] = ProjectVisibility.PRIVATE

class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    industry: Optional[str] = None
    language: Optional[str] = None
    visibility: Optional[ProjectVisibility] = None
    status: Optional[ProjectStatus] = None

class ProjectResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: ProjectStatus
    template_id: Optional[str]
    industry: Optional[str]
    language: str
    visibility: ProjectVisibility
    created_at: datetime
    updated_at: datetime
    last_exported_at: Optional[datetime]
    
    class Config:
        orm_mode = True

class PaginationParams(BaseModel):
    total: int
    skip: int
    limit: int
    has_more: bool

class ProjectListResponse(BaseModel):
    data: List[ProjectResponse]
    pagination: PaginationParams
