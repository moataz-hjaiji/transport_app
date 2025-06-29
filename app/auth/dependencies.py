from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.admin import Admin
from app.auth.auth_handler import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    print("token : ",token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token_data = decode_token(token)  
        print("token_data : ",token_data)
        admin = db.query(Admin).filter(Admin.email == token_data.email).first()
        print(admin,token_data,token)
        if not admin or not admin.is_active:
            raise credentials_exception
            
        return admin
        
    except Exception as e:
        raise credentials_exception from e