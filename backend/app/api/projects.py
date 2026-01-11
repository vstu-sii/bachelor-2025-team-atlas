from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import uuid

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.project import Project, ProjectStatus
from app.schemas.project import (
    ProjectCreate, 
    ProjectUpdate, 
    ProjectResponse,
    ProjectListResponse,
    PaginationParams
)

router = APIRouter()

@router.get("/", response_model=ProjectListResponse)
async def get_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    status: Optional[ProjectStatus] = None,
    sort: str = Query("created_at_desc", regex="^(created_at|updated_at)_(asc|desc)$")
):
    """
    Получить список проектов пользователя с пагинацией
    """
    # Формируем запрос
    query = db.query(Project).filter(Project.user_id == current_user.id)
    
    # Фильтрация по статусу
    if status:
        query = query.filter(Project.status == status)
    
    # Сортировка
    sort_field, sort_order = sort.split("_")
    if sort_field == "created_at":
        order_field = Project.created_at
    else:
        order_field = Project.updated_at
    
    if sort_order == "desc":
        query = query.order_by(order_field.desc())
    else:
        query = query.order_by(order_field.asc())
    
    # Получаем общее количество
    total = query.count()
    
    # Пагинация
    projects = query.offset(skip).limit(limit).all()
    
    return ProjectListResponse(
        data=[ProjectResponse.from_orm(p) for p in projects],
        pagination={
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": skip + limit < total
        }
    )

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Создать новый проект
    """
    # Проверяем лимит проектов
    projects_count = db.query(Project).filter(
        Project.user_id == current_user.id,
        Project.status != ProjectStatus.ARCHIVED
    ).count()
    
    if projects_count >= current_user.projects_limit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Project limit reached ({current_user.projects_limit})"
        )
    
    # Создаем проект
    project = Project(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        title=project_data.title,
        description=project_data.description,
        industry=project_data.industry,
        language=project_data.language,
        visibility=project_data.visibility or ProjectVisibility.PRIVATE
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return ProjectResponse.from_orm(project)

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить детальную информацию о проекте
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
    
    return ProjectResponse.from_orm(project)

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Обновить информацию о проекте
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
    
    # Обновляем поля
    update_data = project_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return ProjectResponse.from_orm(project)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Удалить проект
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
    
    db.delete(project)
    db.commit()
    
    return None
