# app/models/station.py
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from app.database.database import Base

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(Geometry(geometry_type='POINT', srid=4326))  # SRID 4326 = WGS 84 (GPS)
