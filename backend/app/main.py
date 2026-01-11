from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging

from app.api import auth, projects, files, ai, export, templates
from app.core.config import settings
from app.core.database import engine
from app.models import Base

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Создание таблиц в БД (для разработки)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AutoPitch Deck Generator API",
    description="API для автоматической генерации питч-презентаций стартапов",
    version="1.0.0",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтирование статических файлов
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

# Регистрация роутеров
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(files.router, prefix="/api/v1/files", tags=["Files"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI Operations"])
app.include_router(export.router, prefix="/api/v1/export", tags=["Export"])
app.include_router(templates.router, prefix="/api/v1/templates", tags=["Templates"])

@app.get("/")
async def root():
    return {
        "message": "AutoPitch Deck Generator API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/health"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-15T10:00:00Z"}

@app.get("/api/info")
async def api_info():
    return {
        "name": "AutoPitch Deck Generator",
        "description": "API для генерации питч-презентаций",
        "version": "1.0.0",
        "features": [
            "AI-оптимизация презентаций",
            "Генерация с нуля",
            "Профессиональные шаблоны",
            "Экспорт в PPTX/PDF"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
