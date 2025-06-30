from pydantic import BaseModel
from typing import Optional

class StationBase(BaseModel):
    name: str
    code: str
    latitude: float  # For input only - converted to geom in DB
    longitude: float
    address: Optional[str] = None
    station_type: Optional[str] = None
    wheelchair_accessible: bool = False

class StationOut(StationBase):
    id: int
    distance_km: Optional[float] = None
    walking_time_min: Optional[int] = None

class TravelTimeOut(BaseModel):
    from_station: str
    to_station: str
    distance_km: float
    transport_type: str
    estimated_time_min: int