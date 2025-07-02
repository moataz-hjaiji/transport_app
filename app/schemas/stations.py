# app/schemas/station.py
from pydantic import BaseModel, Field

class StationBase(BaseModel):
    name: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class StationCreate(StationBase):
    pass

class StationOut(StationBase):
    id: int

    class Config:
        from_attributes = True
