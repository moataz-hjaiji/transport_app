from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
# from sqlalchemy.dialects.postgresql import UUID
# from geoalchemy2 import Geometry
from app.database.database import Base

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True)
    # geom = Column(Geometry(geometry_type='POINT', srid=4326))  # PostGIS field for location
    address = Column(String)
    station_type = Column(String)  # 'bus', 'metro', 'train'
    wheelchair_accessible = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)