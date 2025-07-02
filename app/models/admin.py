from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from app.database.database import Base

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    avatar = Column(LargeBinary, nullable=True)  
    is_active = Column(Boolean, default=True)
    class Config:
        from_attributes = True