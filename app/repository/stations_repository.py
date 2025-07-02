from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.functions import ST_Distance, ST_GeographyFromText
import math

class StationCRUD:
    @staticmethod
    def get_nearest_stations(
        db: Session,
        latitude: float,
        longitude: float,
        radius_km: float = 5.0,
        limit: int = 5,
        station_type: str = None
    ):
        # Convert km to meters (PostGIS uses meters for distance)
        radius_meters = radius_km * 1000
        
        # Create a geography point from user location
        point = f"POINT({longitude} {latitude})"
        
        query = db.query(
            Station,
            ST_Distance(
                Station.geom,
                func.ST_GeographyFromText(point)
            ).label("distance")
        )
        # Filter by station type if provided
        if station_type:
            query = query.filter(Station.station_type == station_type)
            
        # Filter active stations within radius
        results = (query
            .filter(Station.is_active == True)
            .order_by("distance")
            .limit(limit)
            .all())
        
        return [
            {
                "station": station,
                "distance_km": round(distance / 1000, 2),
                # Estimated walking time (5km/h walking speed)
                "walking_time_min": math.ceil((distance / 1000) / 5 * 60)
            }
            for station, distance in results
        ]

    @staticmethod
    def get_travel_time_between_stations(
        db: Session,
        station1_id: int,
        station2_id: int,
        transport_type: str = 'bus'
    ):
        """
        Returns estimated travel time between two stations.
        In a real app, this would use historical data or a routing engine.
        """
        # Get both stations
        station1 = db.query(Station).get(station1_id)
        station2 = db.query(Station).get(station2_id)
        
        if not station1 or not station2:
            raise ValueError("One or both stations not found")
        
        # Calculate direct distance
        distance = db.scalar(
            db.query(ST_Distance(station1.geom, station2.geom))
        )
        
        distance_km = distance / 1000
        
        # Simple estimation based on transport type
        speed_kmh = {
            'bus': 25,
            'metro': 35,
            'train': 60,
            'walking': 5
        }.get(transport_type, 25)
        
        travel_time_min = round((distance_km / speed_kmh) * 60)
        
        return {
            "from_station": station1.name,
            "to_station": station2.name,
            "distance_km": round(distance_km, 2),
            "transport_type": transport_type,
            "estimated_time_min": travel_time_min
        }