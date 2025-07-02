# app/routers/stations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.auth_handler import admin_only
from app.models.stations import Station
from app.database.database import get_db
from app.schemas.stations import StationCreate, StationOut
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

router = APIRouter(
    prefix="/stations",
    tags=["stations"],
    dependencies=[admin_only]
)
@router.get("/")
async def get_stations(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    ):
    stations = db.query(Station).offset(skip).limit(limit).all()
    return stations
@router.get("/{station_id}", response_model=StationOut)
def get_station(
    station_id: int,
    db: Session = Depends(get_db)
):
    db_station = db.query(Station).filter(Station.id == station_id).first()
    if not db_station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station with id {station_id} not found"
        )
    
    return db_station
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

@router.put("/{station_id}",response_model=StationOut)
def update_station(station_id: int,data: StationCreate,db: Session = Depends(get_db)):
    db_station = db.query(Station).filter(Station.id == station_id).first()
    if not db_station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station with id {station_id} not found"
        )
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_station, field, value)
    
    # 4. Commit changes
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    
    return db_station
@router.delete("/{admin_id}")
def delete_station(admin_id: int,db: Session = Depends(get_db)):
    db_station = db.query(Station).filter(Station.id == admin_id).first()
    if not db_station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station with id {admin_id} not found"
        )
    db.delete(db_station)
    db.commit()
    return None
