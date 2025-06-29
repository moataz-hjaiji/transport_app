from pydantic import BaseModel, EmailStr, field_validator, SecretStr
from typing import Optional

class AdminCreate(BaseModel):
    email: EmailStr 
    username: str
    password: SecretStr    
    is_active: bool = True  
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v
class AdminOut(BaseModel):
    email: str
    username: str
    is_active: bool
class AdminUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None