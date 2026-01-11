from sqlalchemy import Column, String, Integer, BigInteger, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
import uuid

from app.core.database import Base

class FileSourceType(str, enum.Enum):
    UPLOAD = "upload"
    GENERATED = "generated"
    IMPORTED = "imported"

class FileType(str, enum.Enum):
    PPTX = "pptx"
    PDF = "pdf"

class ParsingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class PresentationFile(Base):
    __tablename__ = "presentation_files"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    version_number = Column(Integer, nullable=False, default=1)
    file_type = Column(Enum(FileType), nullable=False)
    source_type = Column(Enum(FileSourceType), default=FileSourceType.UPLOAD)
    original_filename = Column(String(255))
    file_size = Column(BigInteger)
    storage_path = Column(String(500), nullable=False)
    md5_hash = Column(String(32))
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    parsing_status = Column(Enum(ParsingStatus), default=ParsingStatus.PENDING)
    parsing_started_at = Column(DateTime(timezone=True))
    parsing_completed_at = Column(DateTime(timezone=True))
    parsing_errors = Column(String)
    
    # Relationships
    project = relationship("Project", back_populates="presentation_files")
    slides = relationship("Slide", back_populates="presentation_file", cascade="all, delete-orphan")
    
    __table_args__ = (
        {'unique_together': ('project_id', 'version_number')}
    )
    
    def __repr__(self):
        return f"<PresentationFile(id={self.id}, version={self.version_number}, type={self.file_type})>"
