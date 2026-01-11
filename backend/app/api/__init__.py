# Импорт всех роутеров
from app.api.auth import router as auth_router
from app.api.projects import router as projects_router
from app.api.files import router as files_router
from app.api.ai import router as ai_router
from app.api.export import router as export_router
from app.api.templates import router as templates_router

__all__ = [
    'auth_router',
    'projects_router',
    'files_router',
    'ai_router',
    'export_router',
    'templates_router'
]
