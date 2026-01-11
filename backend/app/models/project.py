from sqlalchemy import Column, String, DateTime, Enum, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
import uuid

from app.core.database import Base

class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    UPLOADED = "uploaded"
    PARSING = "parsing"
    PARSED = "parsed"
    OPTIMIZING = "optimizing"
    READY = "ready"
    EXPORTED = "exported"
    ARCHIVED = "archived"

class ProjectVisibility(str, enum.Enum):
    PRIVATE = "private"
    TEAM = "team"
    PUBLIC = "public"

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False, default="Новая презентация")
    description = Column(String)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.DRAFT)
    template_id = Column(String(100), default="default")
    industry = Column(String(100))
    language = Column(String(2), default="ru")
    visibility = Column(Enum(ProjectVisibility), default=ProjectVisibility.PRIVATE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_exported_at = Column(DateTime(timezone=True))
    metadata = Column(JSON, default=lambda: {})
    
    # Relationships
    user = relationship("User", back_populates="projects")
    presentation_files = relationship("PresentationFile", back_populates="project", cascade="all, delete-orphan")
    ai_operations = relationship("AIOperation", back_populates="project", cascade="all, delete-orphan")
    exports = relationship("Export", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, title={self.title}, status={self.status})>"
