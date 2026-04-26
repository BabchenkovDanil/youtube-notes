from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
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

class NoteCreate(BaseModel):
    text: str
    timestamp: int
    video_id: int

class NoteResponse(BaseModel):
    id: int
    text: str
    timestamp: int
    video_id: int
    owner_id: int
    created_at: datetime