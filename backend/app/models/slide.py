from sqlalchemy import Column, String, Integer, DateTime, Enum, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
import uuid

from app.core.database import Base

class SlideType(str, enum.Enum):
    TITLE = "title"
    PROBLEM = "problem"
    SOLUTION = "solution"
    MARKET = "market"
    PRODUCT = "product"
    BUSINESS_MODEL = "business_model"
    TEAM = "team"
    TRACTION = "traction"
    FINANCIALS = "financials"
    COMPETITORS = "competitors"
    ROADMAP = "roadmap"
    CONTACT = "contact"
    OTHER = "other"

class Slide(Base):
    __tablename__ = "slides"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    version_id = Column(String(36), ForeignKey("presentation_files.id"), nullable=False)
    slide_number = Column(Integer, nullable=False)
    slide_type = Column(Enum(SlideType), default=SlideType.OTHER)
    original_content = Column(JSON, default=lambda: {})
    optimized_content = Column(JSON, default=lambda: {})
    applied_template = Column(JSON, default=lambda: {})
    layout_type = Column(String(50), default="standard")
    ai_feedback = Column(String)
    is_modified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    project = relationship("Project")
    presentation_file = relationship("PresentationFile", back_populates="slides")
    
    __table_args__ = (
        {'unique_together': ('version_id', 'slide_number')}
    )
    
    def __repr__(self):
        return f"<Slide(id={self.id}, number={self.slide_number}, type={self.slide_type})>"
