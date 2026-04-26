from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models import User, Video, Note
from app.schemas import VideoAddRequest, VideoResponse
from app.utils import get_current_user
from app.youtube_service import extract_video_id, get_video_info
from app.kafka_producer import send_video_task
from app.redis_client import redis_client

router = APIRouter(prefix='/video', tags=['videos'])


@router.post('/add')
def add_video(
        request: VideoAddRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    video_id = extract_video_id(request.url)
    if not video_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid YouTube URL"
        )

    existing = db.query(Video).filter(Video.club_id == video_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video already exists"
        )

    send_video_task(video_id, current_user.id)

    return {
        "message": "Video is being processed",
        "video_id": video_id
    }

@router.get('/{video_id}')
def get_video_with_notes(
        video_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    cache_key = f'video:{video_id}'
    cached_data = redis_client.get(cache_key)

    if cached_data:
        print(f'Cache HIT for {cache_key}')
        return json.loads(cached_data)

    print(f'Cache MISS for {cache_key}')

    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    notes = db.query(Note).filter(Note.video_id == video_id).all()
    result = {
        'id': video.id,
        'club_id': video.club_id,
        'title': video.title,
        'description': video.description,
        'thumbnail': video.thumbnail,
        'created_at': video.created_at.isoformat(),
        'owner_id': video.owner_id,
        'notes': [
            {
                'id': note.id,
                'text': note.text,
                'timestamp': note.timestamp,
                'owner_id': note.owner_id
            }
            for note in notes
        ]
    }
    redis_client.setex(cache_key, 300, json.dumps(result))
    return result