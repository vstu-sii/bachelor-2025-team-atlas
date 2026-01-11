from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, Enum, Integer, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base

class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    BUSINESS = "business"

class User(Base):
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    telegram_username = Column(String(255))
    telegram_first_name = Column(String(255))
    telegram_last_name = Column(String(255))
    email = Column(String(255))
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    projects_limit = Column(Integer, default=3)
    export_limit_daily = Column(Integer, default=5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    settings = Column(JSON, default=lambda: {"notifications": True, "theme": "light"})
    
    # Relationships
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    exports = relationship("Export", back_populates="user", cascade="all, delete-orphan")
    usage_stats = relationship("UsageStats", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, telegram={self.telegram_username})>"
