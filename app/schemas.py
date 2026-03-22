from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class VideoAddRequest(BaseModel):
    url: str

class VideoResponse(BaseModel):
    id: int
    club_id: str
    title: str
    description: str
    thumbnail: str
    created_at: datetime
    owner_id: int