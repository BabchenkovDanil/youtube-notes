from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Video
from app.schemas import VideoAddRequest, VideoResponse
from app.utils import get_current_user
from app.youtube_service import extract_video_id, get_video_info

router = APIRouter(prefix='/video', tags=['videos'])

@router.post('/add', response_model=VideoResponse)
def add_video(
        requests: VideoAddRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user())
):
    video_id = extract_video_id(requests.url)
    if not video_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid YouTube URL"
        )
    existing_video = db.query(Video).filter(Video.club_id == video_id).first()
    if existing_video:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video already exists"
        )
    video_info = get_video_info(video_id)
    if not video_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch video info from YouTube"
        )
    new_video = Video(
        club_id=video_id,
        title=video_info['title'],
        description=video_info['description'],
        thumbnail=video_info['thumbnail'],
        owner_id=current_user.id
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return new_video