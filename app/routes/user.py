from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta

from app.database.database import get_db
from app.models.admin import Admin
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema, Token, LoginRequest
from app.auth.auth_handler import (
    get_password_hash, 
    create_access_token, 
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.auth.auth_bearer import JWTBearer

router = APIRouter(prefix="/api/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post("/signup", response_model=UserSchema)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
def login(user: LoginRequest , db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": str(db_user.email),
        "id": str(db_user.id),
        "exp": access_token_expires 
    }
    access_token = create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
@router.get("/me", response_model=UserSchema, dependencies=[Depends(JWTBearer())])
def read_current_user(db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    token_data = decode_token(token)
    db_user = db.query(User).filter(User.username == token_data.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user