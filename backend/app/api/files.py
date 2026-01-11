from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
import hashlib
import uuid
from typing import Optional

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.project import Project, ProjectStatus
from app.models.presentation_file import PresentationFile, FileType, ParsingStatus
from app.workers.tasks import parse_presentation_task
from app.core.config import settings

router = APIRouter()

@router.post("/{project_id}/upload")
async def upload_presentation(
    project_id: str,
    file: UploadFile = File(...),
    source_type: str = Form("upload"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Загрузить файл презентации
    """
    # Проверяем проект
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Проверяем размер файла
    file.file.seek(0, 2)  # Переходим в конец файла
    file_size = file.file.tell()
    file.file.seek(0)  # Возвращаемся в начало
    
    max_size = settings.UPLOAD_FILE_SIZE_LIMIT_MB * 1024 * 1024
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds {settings.UPLOAD_FILE_SIZE_LIMIT_MB}MB limit"
        )
    
    # Проверяем тип файла
    filename = file.filename.lower()
    if not (filename.endswith('.pptx') or filename.endswith('.pdf')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PPTX and PDF files are allowed"
        )
    
    # Определяем тип файла
    file_type = FileType.PPTX if filename.endswith('.pptx') else FileType.PDF
    
    # Вычисляем хэш файла
    file_content = await file.read()
    file_md5 = hashlib.md5(file_content).hexdigest()
    
    # Проверяем дубликат
    existing_file = db.query(PresentationFile).filter(
        PresentationFile.project_id == project_id,
        PresentationFile.md5_hash == file_md5
    ).first()
    
    if existing_file:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="File already exists in this project"
        )
    
    # Создаем имя файла для сохранения
    file_extension = 'pptx' if file_type == FileType.PPTX else 'pdf'
    storage_filename = f"{uuid.uuid4()}.{file_extension}"
    storage_path = os.path.join(settings.UPLOAD_DIR, storage_filename)
    
    # Сохраняем файл
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    with open(storage_path, 'wb') as f:
        f.write(file_content)
    
    # Определяем номер версии
    latest_version = db.query(PresentationFile).filter(
        PresentationFile.project_id == project_id
    ).order_by(PresentationFile.version_number.desc()).first()
    
    version_number = latest_version.version_number + 1 if latest_version else 1
    
    # Создаем запись в БД
    presentation_file = PresentationFile(
        id=str(uuid.uuid4()),
        project_id=project_id,
        version_number=version_number,
        file_type=file_type,
        source_type=source_type,
        original_filename=file.filename,
        file_size=file_size,
        storage_path=storage_path,
        md5_hash=file_md5,
        parsing_status=ParsingStatus.PENDING
    )
    
    db.add(presentation_file)
    
    # Обновляем статус проекта
    project.status = ProjectStatus.UPLOADED
    project.updated_at = func.now()
    
    db.commit()
    db.refresh(presentation_file)
    
    # Запускаем фоновую задачу парсинга
    task = parse_presentation_task.delay(str(presentation_file.id))
    
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "task_id": task.id,
            "message": "File uploaded and parsing started",
            "status_url": f"/api/v1/tasks/{task.id}/status"
        }
    )

@router.get("/{project_id}/versions")
async def get_project_versions(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить историю версий проекта
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    versions = db.query(PresentationFile).filter(
        PresentationFile.project_id == project_id
    ).order_by(PresentationFile.version_number.desc()).all()
    
    return {
        "project_id": project_id,
        "versions": [
            {
                "id": v.id,
                "version_number": v.version_number,
                "file_type": v.file_type,
                "original_filename": v.original_filename,
                "upload_date": v.upload_date,
                "parsing_status": v.parsing_status
            }
            for v in versions
        ]
    }
