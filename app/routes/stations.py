from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from app.schemas.stations import StationOut, TravelTimeOut
from app.models.stations import Station
from app.repository.stations_repository import StationCRUD
from app.database.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/stations", tags=["stations"])

@router.get("/nearest", response_model=list[StationOut])
def get_nearest_stations(
    lat: float,
    lng: float,
    radius_km: Optional[float] = 5.0,
    limit: Optional[int] = 5,
    type: Optional[str] = None,  # 'bus', 'metro', 'train'
    db: Session = Depends(get_db)
):
    """
    Find nearest stations within radius (km) of given coordinates.
    Returns stations with walking time estimates.
    """
    try:
        return StationCRUD.get_nearest_stations(
            db=db,
            latitude=lat,
            longitude=lng,
            radius_km=radius_km,
            limit=limit,
            station_type=type
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/travel-time", response_model=TravelTimeOut)
def get_travel_time(
    from_station_id: int,
    to_station_id: int,
    transport_type: str = 'bus',
    db: Session = Depends(get_db)
):
    """
    Get estimated travel time between two stations.
    """
    try:
        return StationCRUD.get_travel_time_between_stations(
            db=db,
            station1_id=from_station_id,
            station2_id=to_station_id,
            transport_type=transport_type
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))