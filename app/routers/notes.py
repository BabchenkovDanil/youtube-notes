from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Note, Video
from app.schemas import NoteCreate, NoteResponse
from app.utils import get_current_user



router = APIRouter(prefix='/notes', tags=['notes'])

@router.post('/', response_model=NoteResponse)
def create_note(
        note_data: NoteCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    video = db.query(Video).filter(Video.id == note_data.video_id).first()
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    new_note = Note(
        text=note_data.text,
        timestamp=note_data.timestamp,
        video_id=note_data.video_id,
        owner_id=current_user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return {
        'id': new_note.id,
        'text': new_note.text,
        'timestamp': new_note.timestamp,
        'video_id': new_note.video_id,
        'owner_id': new_note.owner_id,
        'created_at': new_note.created_at
    }