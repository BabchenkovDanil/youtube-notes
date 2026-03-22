from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, Token
from app.utils import get_password_hash, verify_password, create_access_token, get_current_user
from app.redis_client import save_session, delete_session

from datetime import datetime, timezone

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/register', response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password =  get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token(data={'sub': new_user.email})
    return{'access_token': access_token, 'token_type': 'bearer'}

@router.post('/login', response_model=Token)
def login(user_data: UserLogin, db: Depends(get_db)):
    user = db.query(User).filter(User.mail == user_data.mail).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    save_session(user.id, {
        'user_id': user.id,
        'email': user.email,
        'login_time': datetime.now(timezone.utc).isoformat()
    })


    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.post('/logout')
def logout(current_user: User = Depends(get_current_user)):
    delete_session(current_user.id)
    return {'massage': 'Logged out successfully'}
