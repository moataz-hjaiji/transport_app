# app/routers/stations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.stations import Station
from app.database.database import get_db
from app.schemas.stations import StationCreate, StationOut
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

router = APIRouter(
    prefix="/stations",
    tags=["stations"]
)

@router.post("/", response_model=StationOut)
def create_station(station: StationCreate, db: Session = Depends(get_db)):
    point = from_shape(Point(station.longitude, station.latitude), srid=4326)

    db_station = Station(name=station.name, location=point)
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    return StationOut(
        id=db_station.id,
        name=db_station.name,
        latitude=station.latitude,
        longitude=station.longitude
    )
