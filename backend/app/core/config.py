from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Application
    DEBUG: bool = True
    APP_NAME: str = "AutoPitch Deck Generator"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "postgresql://autopitch_user:password@localhost:5432/autopitch"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Telegram
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    
    # AI Providers
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # File Storage
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    S3_BUCKET_NAME: str = "autopitch-uploads"
    S3_REGION: str = "us-east-1"
    
    # Security
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    UPLOAD_FILE_SIZE_LIMIT_MB: int = 100
    
    # Paths
    UPLOAD_DIR: str = "uploads"
    TEMPLATE_DIR: str = "templates"
    EXPORT_DIR: str = "exports"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
