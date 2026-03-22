from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(String(50), nullable=False)
    tittle = Column(String(255), nullable=False)
    description = Column(String)
    thumbnail = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)
    video_id = Column(Integer, ForeignKey('videos.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    video = relationship('Video')
    user = relationship('User')