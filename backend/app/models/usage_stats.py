from sqlalchemy import Column, BigInteger, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base

class UsageStats(Base):
    __tablename__ = "usage_stats"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    projects_created = Column(Integer, default=0)
    files_uploaded = Column(Integer, default=0)
    ai_operations = Column(Integer, default=0)
    exports_count = Column(Integer, default=0)
    tokens_used_total = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="usage_stats")
    
    __table_args__ = (
        {'unique_together': ('user_id', 'date')}
    )
    
    def __repr__(self):
        return f"<UsageStats(user={self.user_id}, date={self.date}, projects={self.projects_created})>"
