from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import Boolean
from sqlalchemy.orm import Session

from app.schemas import TokenData
from app.database import get_db
from app.models import User
from app.redis_client import get_session, refresh_session

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


SECRET_KEY = 'mysecretkey'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def get_password_hash(password: str) -> str:
    if len(password) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    print("=== VERIFY_TOKEN DEBUG ===")
    print(f"Token: {token[:50]}...")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Payload: {payload}")
        email: str = payload.get('sub')
        print(f"Email from payload: {email}")
        if email is None:
            return None
        return email
    except JWTError as e:
        print(f"JWTError: {e}")
        return None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("=== GET_CURRENT_USER DEBUG ===")
    print(f"Token: {token[:50]}...")
    email = verify_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = db.query(User).filter(User.email == email).first()
    print(f"User found: {user.id if user else 'None'}")
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    session = get_session(user.id)
    print(f"Session from Redis: {session}")
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or not found"
        )
    refresh_session(user.id)

    return user