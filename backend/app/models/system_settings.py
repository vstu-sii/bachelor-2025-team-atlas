from sqlalchemy import Column, String, DateTime, Boolean, JSON, BigInteger
from sqlalchemy.sql import func

from app.core.database import Base

class SystemSettings(Base):
    __tablename__ = "system_settings"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    setting_key = Column(String(100), unique=True, nullable=False)
    setting_value = Column(JSON)
    description = Column(String)
    is_public = Column(Boolean, default=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<SystemSettings(key={self.setting_key}, public={self.is_public})>"
