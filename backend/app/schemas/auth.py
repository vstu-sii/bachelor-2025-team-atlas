from pydantic import BaseModel
from typing import Optional, Dict, Any

class TelegramAuthRequest(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str

class UserResponse(BaseModel):
    id: int
    telegram_username: Optional[str]
    first_name: str
    subscription_tier: str

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse

class RefreshTokenRequest(BaseModel):
    refresh_token: str
