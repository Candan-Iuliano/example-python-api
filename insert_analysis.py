import json
from app.database import SessionLocal
from app.models import Location, AnalysisResult
from sqlalchemy import select
from app.logging_config import get_logger
import math


def city_distance(city_name1: str, city_name2: str):
    session = SessionLocal()
    logger = get_logger()
    try:
        query = select(Location).where(Location.name.in_([city_name1, city_name2]))
        result = session.execute(query) #executes the query and retrieves the data
        output = result.scalars().all()
        if len(output) < 2:
            logger.warning("Invalid location skipped",extra={"event": "city_dstance_failed", "reason": "not all cities could be found"})
            raise ValueError("One or both cities could not be found")
        
        locations = {location.name: location for location in output}
        distance = calculate_distance(locations[city_name1].latitude, locations[city_name1].longitude, locations[city_name2].latitude, locations[city_name2].longitude)
        analysis = {
            "origin_id": locations[city_name1].id,
            "dest_id": locations[city_name2].id,
            "analysis_type": "distance",
            "result": {
                "distance": distance,
                "unit": "km"
            }
        }

        analysis_result = AnalysisResult(**analysis)
        session.add(analysis_result)
        session.commit()
    finally:
        session.close()



def retrieve_analysis_results():
    session = SessionLocal()
    logger = get_logger()
    try:
        query = select(AnalysisResult)
        result = session.execute(query) #executes the query and retrieves the data
        output = result.scalars().all()
        for analysis in output:
            print(analysis.origin.name,"->",analysis.destination.name,":", analysis.result["distance"], analysis.result["unit"])
    finally:
        session.close()



def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    delta_lat = lat2 - lat1
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


# city_distance("Boston", "New York")
# city_distance("New York", "Boston")
retrieve_analysis_results()