from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
    verify_telegram_auth
)
from app.models.user import User
from app.schemas.auth import TelegramAuthRequest, AuthResponse, RefreshTokenRequest
from app.core.config import settings

router = APIRouter()
security = HTTPBearer()

@router.post("/telegram", response_model=AuthResponse)
async def telegram_auth(
    auth_data: TelegramAuthRequest,
    db: Session = Depends(get_db)
):
    """
    Аутентификация через Telegram Widget
    """
    # Проверяем верификацию данных Telegram
    if not verify_telegram_auth(auth_data.dict(), settings.TELEGRAM_BOT_TOKEN):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Telegram authentication data"
        )
    
    # Ищем пользователя или создаем нового
    user = db.query(User).filter(User.telegram_id == auth_data.id).first()
    
    if not user:
        user = User(
            telegram_id=auth_data.id,
            telegram_username=auth_data.username,
            telegram_first_name=auth_data.first_name,
            telegram_last_name=auth_data.last_name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Обновляем последний вход
        user.last_login = func.now()
        db.commit()
    
    # Создаем токены
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user={
            "id": user.id,
            "telegram_username": user.telegram_username,
            "first_name": user.telegram_first_name,
            "subscription_tier": user.subscription_tier
        }
    )

@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Обновление access токена по refresh токену
    """
    try:
        payload = verify_token(token_data.refresh_token)
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Создаем новые токены
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user={
                "id": user.id,
                "telegram_username": user.telegram_username,
                "first_name": user.telegram_first_name,
                "subscription_tier": user.subscription_tier
            }
        )
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Выход из системы (инвалидация токена)
    """
    # В реальном приложении нужно добавить токен в blacklist
    return {"message": "Successfully logged out"}

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency для получения текущего пользователя
    """
    try:
        token = credentials.credentials
        payload = verify_token(token)
        
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        return user
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
