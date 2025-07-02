from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer

from app.database.database import get_db
from app.models.admin import Admin
from app.schemas.user import UserCreate, User as UserSchema, Token
from app.auth.auth_handler import (
    get_password_hash, 
    create_access_token, 
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.auth.auth_bearer import JWTBearer

router = APIRouter()

@router.post("/signup", response_model=UserSchema)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Create new user
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
def login(user: UserCreate, db: Session = Depends(get_db)):
    # Authenticate user
    db_user = db.query(Admin).filter(Admin.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserSchema, dependencies=[Depends(JWTBearer())])
def read_current_user(db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    from app.auth.auth_handler import decode_token
    token_data = decode_token(token)
    db_user = db.query(User).filter(User.username == token_data.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user