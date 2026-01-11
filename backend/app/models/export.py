from sqlalchemy import Column, String, BigInteger, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
import uuid

from app.core.database import Base

class ExportFormat(str, enum.Enum):
    PPTX = "pptx"
    PDF = "pdf"
    BOTH = "both"

class ExportType(str, enum.Enum):
    FULL = "full"
    SUMMARY = "summary"
    PITCH = "pitch"

class ExportQuality(str, enum.Enum):
    STANDARD = "standard"
    HIGH = "high"

class ExportStatus(str, enum.Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Export(Base):
    __tablename__ = "exports"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    export_format = Column(Enum(ExportFormat), nullable=False)
    export_type = Column(Enum(ExportType), default=ExportType.FULL)
    quality = Column(Enum(ExportQuality), default=ExportQuality.STANDARD)
    file_size = Column(BigInteger)
    download_url = Column(String(500))
    expires_at = Column(DateTime(timezone=True))
    status = Column(Enum(ExportStatus), default=ExportStatus.PROCESSING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    project = relationship("Project", back_populates="exports")
    user = relationship("User", back_populates="exports")
    
    def __repr__(self):
        return f"<Export(id={self.id}, format={self.export_format}, status={self.status})>"
