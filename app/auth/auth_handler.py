from datetime import datetime, timedelta
from typing import Optional
from pydantic import  SecretStr
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.token import TokenData
from app.models.admin import Admin
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

auth_scheme = HTTPBearer()


load_dotenv()



# Security
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str| SecretStr):
    if isinstance(password, SecretStr):
        password = password.get_secret_value()
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode with security checks
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])


        print("sub : ",sub)

        if datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Return TokenData with email (assuming "sub" is the email)
        return TokenData(
            email=sub,  # or payload.get("email") if stored separately
            scopes=payload.get("scopes", []),
            exp=datetime.fromtimestamp(payload["exp"])
        )
        
    except JWTError as e:
        if "expired" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e
async def get_current_admin(db: Session = Depends(get_db),token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        print('id',payload.get('id'))
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    db_user = db.query(Admin).filter(Admin.id == payload.get('id')).first()
    print('admin ', db_user)
    if db_user is None:
        raise credentials_exception
    
    return db_user

admin_only = Depends(get_current_admin)