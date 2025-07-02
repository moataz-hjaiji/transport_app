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

class DriverCreate(DriverBase):
    password: constr(min_length=8)  

class DriverUpdate(BaseModel):
    first_name: Optional[constr(max_length=100)]
    last_name: Optional[constr(max_length=100)]
    email: Optional[EmailStr]
    status: Optional[DriverStatusEnum]

class DriverOut(DriverBase):
    id: int
    created_at: datetime
    updated_at: datetime
    status: Optional[DriverStatusEnum]

    class Config:
        orm_mode = True
