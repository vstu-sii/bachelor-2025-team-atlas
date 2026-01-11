from sqlalchemy import Column, String, DateTime, Enum, Boolean, JSON
from sqlalchemy.sql import func

from app.core.database import Base

class TemplateCategory(str, enum.Enum):
    PROFESSIONAL = "professional"
    CREATIVE = "creative"
    MINIMAL = "minimal"
    CORPORATE = "corporate"
    STARTUP = "startup"

class Template(Base):
    __tablename__ = "templates"
    
    id = Column(String(100), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String)
    category = Column(Enum(TemplateCategory), default=TemplateCategory.PROFESSIONAL)
    industry_focus = Column(JSON, default=lambda: [])
    config_schema = Column(JSON, nullable=False)
    thumbnail_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    version = Column(String(20), default="1.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Template(id={self.id}, name={self.name}, category={self.category})>"
