from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Enum, TIMESTAMP, func
import enum
from app.database.database import Base



class DriverStatusEnum(str, enum.Enum):
    inactive = 'inactive'
    active = 'active'
    on_shift = 'on_shift'

class Driver(Base):
    __tablename__ = 'driver'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())