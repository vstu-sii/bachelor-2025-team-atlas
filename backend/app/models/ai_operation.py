from sqlalchemy import Column, String, Integer, DateTime, Enum, Boolean, ForeignKey, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
import uuid

from app.core.database import Base

class OperationType(str, enum.Enum):
    PARSE = "parse"
    OPTIMIZE = "optimize"
    GENERATE = "generate"
    DESIGN = "design"
    ANALYZE_MARKET = "analyze_market"

class OperationStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AIOperation(Base):
    __tablename__ = "ai_operations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    operation_type = Column(Enum(OperationType), nullable=False)
    status = Column(Enum(OperationStatus), default=OperationStatus.PENDING)
    llm_model = Column(String(50), default="gpt-4")
    prompt_version = Column(String(20), default="1.0")
    input_data = Column(JSON, default=lambda: {})
    output_data = Column(JSON, default=lambda: {})
    tokens_used = Column(Integer, default=0)
    processing_time_ms = Column(Integer)
    cost_estimate = Column(Float, default=0.0)
    error_message = Column(String)
    retry_count = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    project = relationship("Project", back_populates="ai_operations")
    
    def __repr__(self):
        return f"<AIOperation(id={self.id}, type={self.operation_type}, status={self.status})>"
