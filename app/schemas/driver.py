from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional
from enum import Enum

class DriverStatusEnum(str, Enum):
    inactive = 'inactive'
    active = 'active'
    on_shift = 'on_shift'

class DriverBase(BaseModel):
    first_name: constr(max_length=100)
    last_name: constr(max_length=100)
    email: EmailStr
    is_active: bool

class DriverCreate(DriverBase):
    password: constr(min_length=8)  
    is_active: Optional[bool] = True

class DriverUpdate(BaseModel):
    first_name: Optional[constr(max_length=100)]
    last_name: Optional[constr(max_length=100)]
    email: Optional[EmailStr]

class DriverOut(DriverBase):
    id: int
    created_at: datetime
    updated_at: datetime
    

    class Config:
        from_attributes = True
