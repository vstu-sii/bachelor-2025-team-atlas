from sqlalchemy import Column, String, Integer, DateTime, BigInteger
from sqlalchemy.sql import func

from app.core.database import Base

class AICache(Base):
    __tablename__ = "ai_cache"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    prompt_hash = Column(String(64), nullable=False)
    model = Column(String(50), nullable=False)
    prompt_version = Column(String(20), nullable=False)
    response_json = Column(JSON, nullable=False)
    tokens_used = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_accessed = Column(DateTime(timezone=True), server_default=func.now())
    access_count = Column(Integer, default=0)
    
    __table_args__ = (
        {'unique_together': ('prompt_hash', 'model', 'prompt_version')}
    )
    
    def __repr__(self):
        return f"<AICache(hash={self.prompt_hash[:8]}..., model={self.model})>"
